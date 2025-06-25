import tkinter as tk
from tkinter import messagebox
from datetime import datetime
import json
import os

class Equipos_Form:
    def __init__(self, panel_principal):
        self.panel_principal = panel_principal
        self.frame = tk.Frame(panel_principal)
        self.frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        tk.Label(self.frame, text="Registrar Nuevo Equipo", font=("Arial", 16)).grid(row=0, column=0, columnspan=2, pady=10)

        self.entries = {}

        campos = [
            ("Código único del dispositivo", "codigo"),
            ("Nombre del propietario", "propietario"),
            ("Ubicación", "ubicacion"),
            ("Ubicación con señas", "senias"),
            ("Fecha de adquisición (YYYY-MM-DD)", "fecha"),
            ("Contraseña del cliente", "contrasena")
        ]

        for idx, (label_text, key) in enumerate(campos):
            tk.Label(self.frame, text=label_text).grid(row=idx+1, column=0, sticky="e", padx=5, pady=5)
            entry = tk.Entry(self.frame, width=30, show="*" if key == "contrasena" else None)
            entry.grid(row=idx+1, column=1, padx=5, pady=5)
            self.entries[key] = entry

        tk.Button(self.frame, text="Guardar Ficha", command=self.guardar_ficha, bg="#4CAF50", fg="white").grid(row=len(campos)+1, column=0, columnspan=2, pady=15)

    def guardar_ficha(self):
        codigo = self.entries["codigo"].get().strip()
        propietario = self.entries["propietario"].get().strip()
        fecha = self.entries["fecha"].get().strip()

        if not codigo or not propietario:
            messagebox.showerror("Error", "Los campos Código y Propietario son obligatorios.")
            return

        # Validación de fecha
        try:
            datetime.strptime(fecha, "%Y-%m-%d")
        except ValueError:
            messagebox.showerror("Error", "La fecha debe tener el formato YYYY-MM-DD.")
            return

        # Creando el diccionario que contiene a la ficha
        ficha = {key: entry.get().strip() for key, entry in self.entries.items()}

        
        archivo_json = "DB/Archivos/TarjetasEquipos.JSON"

        # Leer el los datos del archivo si ya existe
        if os.path.exists(archivo_json):
            with open(archivo_json, "r", encoding="utf-8") as file:
                try:
                    data = json.load(file)
                    if not isinstance(data, list):
                        data = []
                except json.JSONDecodeError:
                    data = []
        else:
            data = []

        data.append(ficha)

        # Guardar en el JSON
        with open(archivo_json, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4, ensure_ascii=False)

        messagebox.showinfo("Éxito", f"El dispositivo '{codigo}' ha sido registrado correctamente.")

        # Limpiar el formulario
        for entry in self.entries.values():
            entry.delete(0, tk.END)
