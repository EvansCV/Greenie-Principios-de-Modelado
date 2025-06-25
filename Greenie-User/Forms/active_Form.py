import tkinter as tk
from config import COLOR_BACKGROUND

class Active_Form():
    def __init__(self, panel_principal,arduino):
        self.arduino = arduino
        self.panel_central = tk.Frame(panel_principal)
        self.panel_central.pack(side=tk.BOTTOM, fill="both", expand=True)

        self.panel_sup = tk.Frame(panel_principal)
        self.panel_sup.pack(side=tk.BOTTOM,fill=tk.X, expand=False)

        self.lblActivadores = tk.Label(self.panel_sup, text="Activadores")
        self.lblActivadores.config(fg="#222d33", font=("Roboto", 15), bg=COLOR_BACKGROUND)
        self.lblActivadores.pack(side=tk.TOP, fill="both", expand=True)

        #----------------------------------------------

        self.lblLuces = tk.Label(self.panel_central, text="Luces de crecimiento")
        self.lblLuces.config(fg="#222d33", font=("Roboto", 15),justify="center")
        self.lblLuces.grid(row=0, column=0, padx=30, pady=1,columnspan=2)

        self.btn_led_on = tk.Button(self.panel_central, text="ON", command=lambda: self.arduino.enviar_comando("luces",True),padx=30)
        self.btn_led_on.grid(row=1, column=0, padx=30, pady=5)

        self.btn_led_off = tk.Button(self.panel_central, text="OFF", command=lambda: self.arduino.enviar_comando("luces",False),padx=30)
        self.btn_led_off.grid(row=1, column=1, padx=30, pady=5)

        #----------------------------------------------

        self.lblVent = tk.Label(self.panel_central, text="Ventilacion")
        self.lblVent.config(fg="#222d33", font=("Roboto", 15),justify="center")
        self.lblVent.grid(row=2, column=0, padx=20, pady=1,columnspan=2)

        self.btn_Vent_on = tk.Button(self.panel_central, text="ON", command=lambda: self.arduino.enviar_comando("vent",True),padx=30)
        self.btn_Vent_on.grid(row=3, column=0, padx=20, pady=5)

        self.btn_Vent_off = tk.Button(self.panel_central, text="OFF", command=lambda: self.arduino.enviar_comando("vent",False),padx=30)
        self.btn_Vent_off.grid(row=3, column=1, padx=20, pady=5)

        # ----------------------------------------------

        self.lblTecho = tk.Label(self.panel_central, text="Compuerta superior")
        self.lblTecho.config(fg="#222d33", font=("Roboto", 15),justify="center")
        self.lblTecho.grid(row=4, column=0, padx=20, pady=1,columnspan=2)

        self.btn_Techo_open = tk.Button(self.panel_central, text="OPEN", command=lambda: self.arduino.enviar_comando("techo",True),padx=23)
        self.btn_Techo_open.grid(row=5, column=0, padx=20, pady=5)

        self.btn_Techo_close = tk.Button(self.panel_central, text="CLOSE", command=lambda: self.arduino.enviar_comando("techo",False),padx=23)
        self.btn_Techo_close.grid(row=5, column=1, padx=20, pady=5)

        # ----------------------------------------------

        self.lblRiego = tk.Label(self.panel_central, text="Sistema de Riego")
        self.lblRiego.config(fg="#222d33", font=("Roboto", 15),justify="center")
        self.lblRiego.grid(row=6, column=0, padx=20, pady=1,columnspan=2)

        self.btn_Riego_open = tk.Button(self.panel_central, text="OPEN", command=lambda: self.arduino.enviar_comando("riego",True),padx=23)
        self.btn_Riego_open.grid(row=7, column=0, padx=18, pady=5)

        self.btn_Riego_close = tk.Button(self.panel_central, text="CLOSE", command=lambda: self.arduino.enviar_comando("riego",False),padx=23)
        self.btn_Riego_close.grid(row=7, column=1, padx=18, pady=5)

        # ----------------------------------------------

        self.lblSistema = tk.Label(self.panel_central, text="Sistema de Automatico")
        self.lblSistema.config(fg="#222d33", font=("Roboto", 15),justify="center")
        self.lblSistema.grid(row=8, column=0, padx=20, pady=1,columnspan=2)

        self.btn_Sistema_on = tk.Button(self.panel_central, text="ON", command=lambda: self.arduino.habilitar_Sistema(True),padx=30)
        self.btn_Sistema_on.grid(row=9, column=0, padx=20, pady=5)

        self.btn_Sistema_off = tk.Button(self.panel_central, text="OFF", command=lambda: self.arduino.habilitar_Sistema(False),padx=30)
        self.btn_Sistema_off.grid(row=9, column=1, padx=20, pady=5)