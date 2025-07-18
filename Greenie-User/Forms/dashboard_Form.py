import tkinter as tk
from config import COLOR_BACKGROUND

class DashboardForm():

    def __init__(self, panel_principal):
        self.panel_inf = tk.Frame(panel_principal)
        self.panel_inf.pack(side=tk.BOTTOM, fill="both", expand=False)

        self.panel_central = tk.Frame(panel_principal)
        self.panel_central.pack(side=tk.BOTTOM, fill="both", expand=True)

        self.panel_sup = tk.Frame(panel_principal)
        self.panel_sup.pack(side=tk.BOTTOM, fill=tk.X, expand=False)

        # ----------------------------

        self.lblDatos = tk.Label(self.panel_sup, text="Datos")
        self.lblDatos.config(fg="#222d33", font=("Roboto", 15), bg=COLOR_BACKGROUND)
        self.lblDatos.pack(side=tk.TOP, fill="both", expand=True)

        #----------------------------

        self.lblTemp = tk.Label(self.panel_central, text="Temperatura: ")
        self.lblTemp.config(fg="#222d33", font=("Roboto", 15))
        self.lblTemp.grid(row=0, column=0, padx=10, pady=10)

        self.lblTempData = tk.Label(self.panel_central, text="--")
        self.lblTempData.config(fg="#222d33", font=("Roboto", 12))
        self.lblTempData.grid(row=0, column=1, padx=10, pady=10)

        self.lblHumA = tk.Label(self.panel_central, text="Humedad de ambiente: ")
        self.lblHumA.config(fg="#222d33", font=("Roboto", 15))
        self.lblHumA.grid(row=1, column=0, padx=10, pady=10)

        self.lblHumAData = tk.Label(self.panel_central, text="--")
        self.lblHumAData.config(fg="#222d33", font=("Roboto", 12))
        self.lblHumAData.grid(row=1, column=1, padx=10, pady=10)

        self.lblLuz = tk.Label(self.panel_central, text="Luz de ambiente: ")
        self.lblLuz.config(fg="#222d33", font=("Roboto", 15))
        self.lblLuz.grid(row=2, column=0, padx=10, pady=10)

        self.lblLuzData = tk.Label(self.panel_central, text="--")
        self.lblLuzData.config(fg="#222d33", font=("Roboto", 12))
        self.lblLuzData.grid(row=2, column=1, padx=10, pady=10)

        self.lblHumS = tk.Label(self.panel_central, text="Humedad de suelo: ")
        self.lblHumS.config(fg="#222d33", font=("Roboto", 15))
        self.lblHumS.grid(row=3, column=0, padx=10, pady=10)

        self.lblHumSData = tk.Label(self.panel_central, text="--")
        self.lblHumSData.config(fg="#222d33", font=("Roboto", 12))
        self.lblHumSData.grid(row=3, column=1, padx=10, pady=10)

        # ----------------------------
        self.lblAP = tk.Label(self.panel_inf, text="Agua potable: ")
        self.lblAP.config(fg="#222d33", font=("Roboto", 15))
        self.lblAP.grid(row=0, column=0, padx=10, pady=10)

        self.lblAPData = tk.Label(self.panel_inf, text="--")
        self.lblAPData.config(fg="#222d33", font=("Roboto", 12))
        self.lblAPData.grid(row=0, column=1, padx=10, pady=10)

        self.lblAD = tk.Label(self.panel_inf, text="Agua drenada: ")
        self.lblAD.config(fg="#222d33", font=("Roboto", 15))
        self.lblAD.grid(row=1, column=0, padx=10, pady=10)

        self.lblADData = tk.Label(self.panel_inf, text="--")
        self.lblADData.config(fg="#222d33", font=("Roboto", 12))
        self.lblADData.grid(row=1, column=1, padx=10, pady=10)

        # ----------------------------

        self.lblLuces = tk.Label(self.panel_inf, text="Luces: ")
        self.lblLuces.config(fg="#222d33", font=("Roboto", 15))
        self.lblLuces.grid(row=2, column=0, padx=10, pady=10)

        self.lblLucesData = tk.Label(self.panel_inf, text="--")
        self.lblLucesData.config(fg="#222d33", font=("Roboto", 12))
        self.lblLucesData.grid(row=2, column=1, padx=10, pady=10)

        self.lblVent = tk.Label(self.panel_inf, text="Ventilador: ")
        self.lblVent.config(fg="#222d33", font=("Roboto", 15))
        self.lblVent.grid(row=3, column=0, padx=10, pady=10)

        self.lblVentData = tk.Label(self.panel_inf, text="--")
        self.lblVentData.config(fg="#222d33", font=("Roboto", 12))
        self.lblVentData.grid(row=3, column=1, padx=10, pady=10)

        self.lblTapa = tk.Label(self.panel_inf, text="Techo: ")
        self.lblTapa.config(fg="#222d33", font=("Roboto", 15))
        self.lblTapa.grid(row=4, column=0, padx=10, pady=10)

        self.lblTapaData = tk.Label(self.panel_inf, text="--")
        self.lblTapaData.config(fg="#222d33", font=("Roboto", 12))
        self.lblTapaData.grid(row=4, column=1, padx=10, pady=10)

        # ----------------------------

#{"humedadAmbiente":95%,
# "temperatura":24.8C,
# "luzAmbiente":26%,
# "humedadSuelo":15%,

# "aguaPotable":9%,
# "aguaDrenada":1%,

# "luces":true,
# "ventilador":false,
# "tapaSuperior":false}