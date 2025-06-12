import tkinter as tk

from matplotlib import figure
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class GraphicForm():

    def __init__(self, panel_pricipal):
        figura = Figure(figsize=(3, 2), dpi=100)
        ax1 = figura.add_subplot(2, 1, 1)
        ax2 = figura.add_subplot(2, 1, 2)

        figura.subplots_adjust(hspace=0.4)

        self.grafico1(ax1)
        self.grafico2(ax2)

        canvas = FigureCanvasTkAgg(figura, master=panel_pricipal)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

    def grafico1(self, ax):
        x = [1, 2, 3, 4, 5]
        y = [2, 4, 6, 8, 10]

        ax.bar(x, y, label='Grafico 1', color="blue", alpha=0.7)

        ax.set_title("Grafico - Temperatura")
        ax.set_xlabel("Tiempo")
        ax.set_ylabel("Temperatura")
        ax.legend()

        for i, v in enumerate(y):
            ax.text(x[i] - 0.1, v + 0.1, str(v), color="black")

        ax.grid(axis="y",linestyle='--', alpha=0.7)

    def grafico2(self, ax):
        x = [1, 2, 3, 4, 5]
        y = [1, 2, 1, 2, 1]

        ax.plot(x, y, label='Grafico 2', color="blue")
        ax.set_title("Grafico - Humedad")
        ax.set_xlabel("Tiempo",fontsize=12)
        ax.set_ylabel("Humedad",fontsize=12)
        #ax.plot(x, y, label='Grafico 3', color="red",linestyle="--",marker="o")
        #ax.annotate('Punto importante', xy=(3, 1), xytext=(3.5, 1.5),
        #            arrowprops=dict(facecolor='black', shrink=0.05))

        ax.set_xlim(0,6)
        ax.set_ylim(0,3)
        ax.grid(True,linestyle='--', alpha=0.6)
        ax.legend()