import tkinter as tk
import csv
from datetime import datetime
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class GraphicForm():
    def __init__(self, panel_principal):
        self.panel_principal = panel_principal
        self.figura = Figure(figsize=(5, 4), dpi=100)
        self.ax = self.figura.add_subplot(1, 1, 1)  # Solo un gráfico
        self.figura.subplots_adjust(hspace=0.4)

        # Menú desplegable
        opciones = ["Humedad ambiente", "Temperatura", "Humedad suelo", "Luz ambiente"]
        self.opcion = tk.StringVar(value=opciones[0])
        top_frame = tk.Frame(panel_principal)
        top_frame.pack(side=tk.TOP, fill=tk.X)
        dropdown = tk.OptionMenu(top_frame, self.opcion, *opciones, command=self.actualizar_graficos)
        dropdown.config(width=20)
        dropdown.pack(side=tk.LEFT, padx=10, pady=5)

        # Canvas de matplotlib
        self.canvas = FigureCanvasTkAgg(self.figura, master=panel_principal)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        # Cargar gráfico inicial
        self.actualizar_graficos(self.opcion.get())

    def actualizar_graficos(self, seleccion):
        self.ax.clear()

        if seleccion == "Humedad ambiente":
            self.grafico_humedad_ambiente(self.ax)
        elif seleccion == "Temperatura":
            self.grafico_temperatura(self.ax)
        elif seleccion == "Humedad suelo":
            self.grafico_humedad_suelo(self.ax)
        elif seleccion == "Luz ambiente":
            self.grafico_luz(self.ax)

        self.canvas.draw()

    def leer_datos(self, path):
        x, y = [], []
        with open(path, 'r') as file:
            lector = csv.reader(file)
            next(lector)  # Saltar encabezado

            try:
                primera = next(lector)
                t0 = datetime.strptime(primera[0] + " " + primera[1], "%Y-%m-%d %H:%M:%S")
                x.append(0)
                y.append(float(primera[2]))

                for fila in lector:
                    t = datetime.strptime(fila[0] + " " + fila[1], "%Y-%m-%d %H:%M:%S")
                    delta = (t - t0).total_seconds() / 60
                    x.append(delta)
                    y.append(float(fila[2]))

            except Exception as e:
                print(f"Error leyendo archivo {path}: {e}")

        return x, y

    def graficar(self, ax, path, color, titulo, ylabel):
        x, y = self.leer_datos(path)
        if len(x) > 0 and len(y) > 0:
            ax.plot(x, y, color=color, label=titulo)
            ax.set_title(titulo)
            ax.set_xlabel("Tiempo (min)")
            ax.set_ylabel(ylabel)
            ax.set_xlim(0, max(x))
            ax.set_ylim(0, max(y) + 1)
            ax.grid(True, linestyle='--', alpha=0.6)
            ax.legend()

    def grafico_humedad_ambiente(self, ax):
        self.graficar(ax, 'DB/Archivos/datahumA.csv', 'blue', 'Humedad del Ambiente', 'Humedad')

    def grafico_temperatura(self, ax):
        self.graficar(ax, 'DB/Archivos/dataTemp.csv', 'red', 'Temperatura', 'Temperatura (°C)')

    def grafico_humedad_suelo(self, ax):
        self.graficar(ax, 'DB/Archivos/datahumS.csv', 'green', 'Humedad del Suelo', 'Humedad')

    def grafico_luz(self, ax):
        self.graficar(ax, 'DB/Archivos/dataLuz.csv', 'purple', 'Luz del Ambiente', 'Nivel de luz')
