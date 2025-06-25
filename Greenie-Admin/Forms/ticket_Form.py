import tkinter as tk
from tkinter import ttk, messagebox
import csv
import os

class TicketForm(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg="white")
        self.pack(fill="both", expand=True)

        tk.Label(self, text="📋 Lista de Tickets Recibidos", font=("Arial", 16), bg="white").pack(pady=10)

        # --- Filtro ---
        filtro_frame = tk.Frame(self, bg="white")
        filtro_frame.pack(pady=5)

        tk.Label(filtro_frame, text="🔍 Filtrar por:", bg="white").pack(side="left", padx=5)

        self.columnas = ["ID", "Fecha", "Usuario", "Nombre", "Teléfono", "Dirección", "Asunto", "Descripción"]
        self.combo_filtro = ttk.Combobox(filtro_frame, values=self.columnas, state="readonly")
        self.combo_filtro.current(0)
        self.combo_filtro.pack(side="left", padx=5)

        self.entry_filtro = tk.Entry(filtro_frame, width=30)
        self.entry_filtro.pack(side="left", padx=5)

        btn_filtrar = tk.Button(filtro_frame, text="Aplicar Filtro", command=self.aplicar_filtro, bg="#17a2b8", fg="white")
        btn_filtrar.pack(side="left", padx=5)

        btn_limpiar = tk.Button(filtro_frame, text="Limpiar", command=self.limpiar_filtro, bg="#6c757d", fg="white")
        btn_limpiar.pack(side="left", padx=5)

        # --- Tabla con Scrollbars ---
        contenedor = tk.Frame(self)
        contenedor.pack(padx=10, pady=10, fill="both", expand=True)

        self.tree = ttk.Treeview(contenedor, columns=self.columnas, show="headings")

        for col in self.columnas:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=150, anchor="center")

        scrollbar_y = ttk.Scrollbar(contenedor, orient="vertical", command=self.tree.yview)
        scrollbar_y.pack(side="right", fill="y")
        self.tree.configure(yscrollcommand=scrollbar_y.set)

        scrollbar_x = ttk.Scrollbar(contenedor, orient="horizontal", command=self.tree.xview)
        scrollbar_x.pack(side="bottom", fill="x")
        self.tree.configure(xscrollcommand=scrollbar_x.set)

        self.tree.pack(side="left", fill="both", expand=True)

        # --- Botón para resolver ---
        tk.Button(self, text="✅ Marcar como resuelto", command=self.resolver_ticket, bg="#007bff", fg="white").pack(pady=10)

        # --- Rutas y datos ---
        self.ruta_tickets = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "Greenie-Data", "tickets.csv"))
        self.ruta_historial = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "Greenie-Data", "historial_tickets.csv"))
        self.todos_los_tickets = []  # se usa para filtrar sin perder los datos originales
        self.cargar_tickets()

    def cargar_tickets(self):
        self.todos_los_tickets.clear()
        self.tree.delete(*self.tree.get_children())

        if not os.path.exists(self.ruta_tickets):
            return

        with open(self.ruta_tickets, "r", newline='', encoding="utf-8") as f:
            reader = csv.reader(f)
            next(reader, None)  # saltar encabezado
            for row in reader:
                self.todos_los_tickets.append(row)
                self.tree.insert("", tk.END, values=row)

    def aplicar_filtro(self):
        filtro_texto = self.entry_filtro.get().strip().lower()
        columna = self.combo_filtro.get()
        if not filtro_texto:
            return

        idx_col = self.columnas.index(columna)

        # Limpiar tabla
        self.tree.delete(*self.tree.get_children())

        for fila in self.todos_los_tickets:
            if filtro_texto in fila[idx_col].lower():
                self.tree.insert("", tk.END, values=fila)

    def limpiar_filtro(self):
        self.entry_filtro.delete(0, tk.END)
        self.cargar_tickets()

    def resolver_ticket(self):
        seleccionado = self.tree.selection()
        if not seleccionado:
            messagebox.showwarning("Aviso", "Selecciona un ticket.")
            return

        item = seleccionado[0]
        datos = self.tree.item(item, "values")

        self.tree.delete(item)

        # Escribir en historial
        if not os.path.exists(self.ruta_historial):
            with open(self.ruta_historial, "w", newline='', encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(self.columnas)

        with open(self.ruta_historial, "a", newline='', encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(datos)

        # Actualizar CSV tickets.csv
        self.todos_los_tickets = [row for row in self.todos_los_tickets if row[0] != datos[0]]
        with open(self.ruta_tickets, "w", newline='', encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(self.columnas)
            writer.writerows(self.todos_los_tickets)

        messagebox.showinfo("✅ Ticket resuelto", "Se movió al historial.")






