import tkinter as tk
import csv
from datetime import datetime
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class GraphicForm():
    def __init__(self, panel_principal):
        self.panel_principal = panel_principal
        self.figura = Figure(figsize=(5, 4), dpi=100)
        self.ax1 = self.figura.add_subplot(2, 1, 1)
        self.ax2 = self.figura.add_subplot(2, 1, 2)
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

        # Cargar gráficos iniciales
        self.actualizar_graficos(self.opcion.get())

    def actualizar_graficos(self, seleccion):
        self.ax1.clear()
        self.ax2.clear()

        if seleccion == "Humedad ambiente":
            self.graficoHumedadA2(self.ax2)
        elif seleccion == "Temperatura":
            self.grafico_temperatura2(self.ax2)
        elif seleccion == "Humedad suelo":
            self.grafico_humedadS2(self.ax2)
        elif seleccion == "Luz ambiente":
            self.grafico_luz2(self.ax2)

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
                    delta = (t - t0).total_seconds() / 60  # Tiempo en minutos desde el primer dato
                    x.append(delta)
                    y.append(float(fila[2]))
                    print(x, y)

            except Exception as e:
                print(f"Error leyendo archivo {path}: {e}")

        print(f"Datos leídos de {path}: x={x}, y={y}")
        return x, y

    def graficoHumedadA2(self, ax):
        x, y = self.leer_datos('DB/Archivos/datahumA.csv')
        if len(x) > 0 and len(y) > 0:
            ax.plot(x, y, label='Gráfico 2', color="blue")
            ax.set_title("Gráfico - Humedad del Ambiente")
            ax.set_xlabel("Tiempo (min)")
            ax.set_ylabel("Humedad")
            ax.set_xlim(0, max(x))
            ax.set_ylim(0, max(y) + 1)
            ax.grid(True, linestyle='--', alpha=0.6)
            ax.legend()

    def grafico_temperatura2(self, ax):
        x, y = self.leer_datos('DB/Archivos/dataTemp.csv')
        if len(x) > 0 and len(y) > 0:
            ax.plot(x, y, label='Gráfico 2', color="red")
            ax.set_title("Gráfico - Temperatura")
            ax.set_xlabel("Tiempo (min)")
            ax.set_ylabel("Temperatura")
            ax.set_xlim(0, max(x))
            ax.set_ylim(0, max(y) + 1)
            ax.grid(True, linestyle='--', alpha=0.6)
            ax.legend()

    def grafico_humedadS2(self, ax):
        x, y = self.leer_datos('DB/Archivos/datahumS.csv')
        if len(x) > 0 and len(y) > 0:
            ax.plot(x, y, label='Gráfico 2', color="green")
            ax.set_title("Gráfico - Humedad del Suelo")
            ax.set_xlabel("Tiempo (min)")
            ax.set_ylabel("Humedad")
            ax.set_xlim(0, max(x))
            ax.set_ylim(0, max(y) + 1)
            ax.grid(True, linestyle='--', alpha=0.6)
            ax.legend()

    def grafico_luz2(self, ax):
        x, y = self.leer_datos('DB/Archivos/dataLuz.csv')
        if len(x) > 0 and len(y) > 0:
            ax.plot(x, y, label='Gráfico 2', color="purple")
            ax.set_title("Gráfico - Luz del Ambiente")
            ax.set_xlabel("Tiempo (min)")
            ax.set_ylabel("Nivel de luz")
            ax.set_xlim(0, max(x))
            ax.set_ylim(0, max(y) + 1)
            ax.grid(True, linestyle='--', alpha=0.6)
            ax.legend()
