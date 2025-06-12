import os
import tkinter as tk
import csv
from datetime import datetime
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from DB.Defaut_Values import default_Values

class GraphicForm():

    def __init__(self, panel_principal):
        self.default_values = default_Values()
        self.panel_principal = panel_principal
        self.figura = Figure(figsize=(2, 3), dpi=100)
        self.ax2 = self.figura.add_subplot(2, 1, 1)
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
        x, y = [],[]
        try:
            ruta = os.path.abspath(path)
            print(f"Leyendo archivo: {ruta}")
            with open(ruta, 'r', newline='') as file:
                lector = csv.reader(file)
                encabezado = next(lector)
                if encabezado[1].lower() == "hora":
                    primera = next(lector)
                else:
                    primera = encabezado

                tiempo_inicial = datetime.strptime(primera[1], "%H:%M:%S").timestamp() / 60
                x.append(0)
                y.append(float(primera[2]))

                for fila in lector:
                    try:
                        tiempo_actual = datetime.strptime(fila[1], "%H:%M:%S").timestamp() / 60
                        x.append(tiempo_actual - tiempo_inicial)
                        y.append(float(fila[2]))
                    except (ValueError, IndexError) as e:
                        print(f"Fila inválida ignorada: {fila} ({e})")
        except Exception as e:
            print(f"Error leyendo {path}: {e}")
        return x, y

    def graficoHumedadA2(self, ax):
        x, y = self.leer_datos(self.default_values.archivo_humA)
        ax.plot(x, y, label='Gráfico 2', color="blue")
        ax.set_title("Gráfico - Humedad del Ambiente")
        ax.set_xlabel("Tiempo (min)")
        ax.set_ylabel("Humedad")
        if x:
            ax.set_xlim(0, max(x))
        if y:
            ax.set_ylim(0, max(y) + 1)
        ax.grid(True, linestyle='--', alpha=0.6)
        ax.legend()


    def grafico_temperatura2(self, ax):
        x, y = self.leer_datos(self.default_values.archivo_Temp)
        ax.plot(x, y, label='Gráfico 2', color="red")
        ax.set_title("Gráfico - Temperatura")
        ax.set_xlabel("Tiempo (min)")
        ax.set_ylabel("Temperatura")
        if x:
            ax.set_xlim(0, max(x))
        if y:
            ax.set_ylim(0, max(y) + 1)
        ax.grid(True, linestyle='--', alpha=0.6)
        ax.legend()


    def grafico_humedadS2(self, ax):
        x, y = self.leer_datos(self.default_values.archivo_humS)
        ax.plot(x, y, label='Gráfico 2', color="green")
        ax.set_title("Gráfico - Humedad del Suelo")
        ax.set_xlabel("Tiempo (min)")
        ax.set_ylabel("Humedad")
        if x:
            ax.set_xlim(0, max(x))
        if y:
            ax.set_ylim(0, max(y) + 1)
        ax.grid(True, linestyle='--', alpha=0.6)
        ax.legend()

    def grafico_luz2(self, ax):
        x, y = self.leer_datos(self.default_values.archivo_Luz)
        ax.plot(x, y, label='Gráfico 2', color="purple")
        ax.set_title("Gráfico - Luz del Ambiente")
        ax.set_xlabel("Tiempo (min)")
        ax.set_ylabel("Nivel de luz")
        if x:
            ax.set_xlim(0, max(x))
        if y:
            ax.set_ylim(0, max(y) + 1)
        ax.grid(True, linestyle='--', alpha=0.6)
        ax.legend()