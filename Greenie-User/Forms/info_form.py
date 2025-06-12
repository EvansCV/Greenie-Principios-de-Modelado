import tkinter as tk
import Util.util_ventana as util_ventana

class InfoForm(tk.Toplevel):

    def __init__(self) -> None:
        super().__init__()
        self.config_window()
        self.construirWidget()

    def config_window(self):
        self.title("Dashboard")
        #self.iconbitmap("./assets/icon.ico")
        w,h=400,100
        util_ventana.centrar_ventana(self,w,h)

    def construirWidget(self):
        self.labelVersion = tk.Label(self, text="Version 1.0")
        self.labelVersion.config(fg="#000000", font=("Roboto", 20),pady=10,width=20)
        self.labelVersion.pack()

        self.labelAutor = tk.Label(self, text="Autor: Adrian Alvarez")
        self.labelAutor.config(fg="#000000", font=("Roboto", 20), pady=10, width=20)
        self.labelAutor.pack()