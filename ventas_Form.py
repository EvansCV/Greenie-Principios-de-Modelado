import tkinter as tk
from tkinter import messagebox
import json
from datetime import datetime
import os

class Ventas_Form:
    def __init__(self, panel_principal):
        self.panel_principal = panel_principal
        self.frame = tk.Frame(panel_principal)
        self.frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        tk.Label(self.frame, text="Listado de Equipos Vendidos", font=("Arial", 16)).pack(pady=10)

        self.lista_frame = tk.Frame(self.frame)
        self.lista_frame.pack(fill=tk.BOTH, expand=True)

        self.tooltip = None  

        self.cargar_fichas()

    def cargar_fichas(self):
        archivo_json = "DB/Archivos/TarjetasEquipos.JSON"

        if not os.path.exists(archivo_json):
            messagebox.showerror("Error", "No se encontró el archivo FichasEquipos.json.")
            return

        try:
            with open(archivo_json, "r", encoding="utf-8") as file:
                fichas = json.load(file)
        except json.JSONDecodeError:
            messagebox.showerror("Error", "Error al leer el archivo JSON.")
            return

        # Se ordenan las ventas según fecha de adquisición
        try:
            fichas.sort(key=lambda x: datetime.strptime(x.get("fecha", "1900-01-01"), "%Y-%m-%d"), reverse=True)
        except Exception as e:
            print("Error ordenando por fecha:", e)

        for ficha in fichas:
            codigo = ficha.get("codigo", "Sin código")
            label = tk.Label(self.lista_frame, text=f"Invernadero: {codigo}", fg="blue", cursor="hand2", font=("Arial", 12))
            label.pack(anchor="w", pady=2)

            # Eventos para mostrar y ocultar la info
            label.bind("<Enter>", lambda e, datos=ficha: self.mostrar_info(e.widget, datos))
            label.bind("<Leave>", lambda e: self.ocultar_info())

    def mostrar_info(self, widget, datos):
        # El tooltip despliega la info cerca del mouse
        if self.tooltip:
            self.tooltip.destroy()

        self.tooltip = tk.Toplevel(self.panel_principal)
        self.tooltip.wm_overrideredirect(True)  
        x = widget.winfo_rootx() + 100
        y = widget.winfo_rooty() + 20
        self.tooltip.wm_geometry(f"+{x}+{y}")

        info_texto = (
            f"Propietario: {datos.get('propietario', '')}\n"
            f"Ubicación: {datos.get('ubicacion', '')}\n"
            f"Señas: {datos.get('senias', '')}\n"
            f"Fecha de adquisición: {datos.get('fecha', '')}\n"
            f"Contraseña: {datos.get('contrasena', '')}"
        )

        label = tk.Label(self.tooltip, text=info_texto, justify="left", background="lightyellow", relief="solid", borderwidth=1, padx=5, pady=5)
        label.pack()

    def ocultar_info(self):
        if self.tooltip:
            self.tooltip.destroy()
            self.tooltip = None
