import tkinter as tk
import csv
import os
from datetime import datetime

class TicketForm(tk.Frame):
    def __init__(self, parent, id_usuario, nombre="", telefono="", direccion=""):
        super().__init__(parent, bg="white")
        self.pack(fill="both", expand=True)

        # Guardar la información del usuario
        self.id_usuario = id_usuario
        self.nombre = nombre
        self.telefono = telefono
        self.direccion = direccion

        tk.Label(self, text="Crear Ticket de Soporte", font=("Arial", 16), bg="white").pack(pady=10)

        # Agregar etiquetas para mostrar la información del usuario
        tk.Label(self, text=f"Nombre: {self.nombre}", bg="white").pack(anchor="w", padx=10)
        tk.Label(self, text=f"Teléfono: {self.telefono}", bg="white").pack(anchor="w", padx=10)
        tk.Label(self, text=f"Dirección: {self.direccion}", bg="white").pack(anchor="w", padx=10)

        tk.Label(self, text="Asunto:", bg="white").pack(anchor="w", padx=10)
        self.entry_asunto = tk.Entry(self, width=50)
        self.entry_asunto.pack(padx=10, pady=5)

        tk.Label(self, text="Descripción:", bg="white").pack(anchor="w", padx=10)
        self.text_descripcion = tk.Text(self, height=6, width=50)
        self.text_descripcion.pack(padx=10, pady=5)

        tk.Button(self, text="Enviar Ticket", command=self.guardar_ticket, bg="#28a745", fg="white").pack(pady=10)

        self.label_confirmacion = tk.Label(self, text="", bg="white", fg="green")
        self.label_confirmacion.pack()

    def guardar_ticket(self):
        asunto = self.entry_asunto.get().strip()
        descripcion = self.text_descripcion.get("1.0", tk.END).strip()
        fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        if asunto and descripcion:
            ruta = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "Greenie-Data", "tickets.csv"))
            os.makedirs(os.path.dirname(ruta), exist_ok=True)
            archivo_existe = os.path.exists(ruta)
            nuevo_id = 1

            if archivo_existe:
                with open(ruta, "r", newline='', encoding="utf-8") as f:
                    reader = csv.reader(f)
                    next(reader, None)
                    filas = list(reader)
                    if filas:
                        nuevo_id = int(filas[-1][0]) + 1

            with open(ruta, "a", newline='', encoding="utf-8") as f:
                writer = csv.writer(f)
                if not archivo_existe:
                    writer.writerow(["ID", "Fecha", "Usuario", "Nombre", "Teléfono", "Dirección", "Asunto", "Descripción"])
                writer.writerow([
                    nuevo_id,
                    fecha,
                    self.id_usuario,
                    self.nombre,
                    self.telefono,
                    self.direccion,
                    asunto,
                    descripcion
                ])

            self.label_confirmacion.config(text="✅ Ticket enviado con éxito.", fg="green")
            self.entry_asunto.delete(0, tk.END)
            self.text_descripcion.delete("1.0", tk.END)
        else:
            self.label_confirmacion.config(text="⚠️ Por favor llena todos los campos.", fg="red")


