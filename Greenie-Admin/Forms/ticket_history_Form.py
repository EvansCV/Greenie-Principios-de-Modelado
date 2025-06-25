import tkinter as tk
from tkinter import ttk
import csv
import os

class TicketHistoryForm(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg="white")
        self.pack(fill="both", expand=True)

        self.columnas = ["ID", "Fecha", "Usuario", "Nombre", "Teléfono", "Dirección", "Asunto", "Descripción"]

        # === Título ===
        tk.Label(self, text="📂 Historial de Tickets", font=("Arial", 16), bg="white").pack(pady=10)

        # === Filtro ===
        filtro_frame = tk.Frame(self, bg="white")
        filtro_frame.pack(pady=5)

        tk.Label(filtro_frame, text="🔍 Filtrar por:", bg="white").pack(side="left", padx=5)

        self.combo_filtro = ttk.Combobox(filtro_frame, values=self.columnas, state="readonly")
        self.combo_filtro.current(0)
        self.combo_filtro.pack(side="left", padx=5)

        self.entry_filtro = tk.Entry(filtro_frame, width=30)
        self.entry_filtro.pack(side="left", padx=5)

        tk.Button(filtro_frame, text="Aplicar Filtro", command=self.aplicar_filtro, bg="#17a2b8", fg="white").pack(side="left", padx=5)
        tk.Button(filtro_frame, text="Limpiar", command=self.limpiar_filtro, bg="#6c757d", fg="white").pack(side="left", padx=5)

        # === Tabla con scroll ===
        contenedor = tk.Frame(self, bg="white")
        contenedor.pack(padx=10, pady=10, fill="both", expand=True)

        self.tree = ttk.Treeview(contenedor, columns=self.columnas, show="headings")
        for col in self.columnas:
            ancho = 150 if col != "Descripción" else 250
            self.tree.heading(col, text=col, anchor="center")
            self.tree.column(col, anchor="center", width=ancho)

        scrollbar_y = ttk.Scrollbar(contenedor, orient="vertical", command=self.tree.yview)
        scrollbar_y.pack(side="right", fill="y")
        self.tree.configure(yscrollcommand=scrollbar_y.set)

        scrollbar_x = ttk.Scrollbar(contenedor, orient="horizontal", command=self.tree.xview)
        scrollbar_x.pack(side="bottom", fill="x")
        self.tree.configure(xscrollcommand=scrollbar_x.set)

        self.tree.pack(side="left", fill="both", expand=True)

        # === Cargar datos ===
        self.ruta_historial = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "Greenie-Data", "historial_tickets.csv"))
        self.todos_los_tickets = []
        self.cargar_datos()

    def cargar_datos(self):
        self.todos_los_tickets.clear()
        self.tree.delete(*self.tree.get_children())

        if not os.path.exists(self.ruta_historial):
            tk.Label(self, text="⚠️ No hay historial aún.", bg="white", fg="gray").pack(pady=10)
            return

        with open(self.ruta_historial, "r", newline='', encoding="utf-8") as f:
            reader = csv.reader(f)
            next(reader, None)  # encabezado
            for row in reader:
                self.todos_los_tickets.append(row)
                self.tree.insert("", tk.END, values=row)

    def aplicar_filtro(self):
        texto = self.entry_filtro.get().strip().lower()
        columna = self.combo_filtro.get()
        if not texto:
            return
        idx = self.columnas.index(columna)

        self.tree.delete(*self.tree.get_children())

        for fila in self.todos_los_tickets:
            if texto in fila[idx].lower():
                self.tree.insert("", tk.END, values=fila)

    def limpiar_filtro(self):
        self.entry_filtro.delete(0, tk.END)
        self.cargar_datos()
