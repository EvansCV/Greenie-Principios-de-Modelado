import tkinter as tk
from config import COLOR_BACKGROUND,COLOR_BACKGROUND2,COLOR_SECUNDARIO
from DB.Defaut_Values import default_Values

class Config_Form():

    def __init__(self,panel_principal):
        self.default_Values = default_Values()
        self.panel_inf = tk.Frame(panel_principal)
        self.panel_inf.pack(side=tk.BOTTOM, fill=tk.X,expand=True)

        self.panel_sup = tk.Frame(panel_principal)
        self.panel_sup.pack(side=tk.BOTTOM, fill=tk.X,expand=False)

        self.lblConfiguracion = tk.Label(self.panel_sup, text="Configuracion")
        self.lblConfiguracion.config(fg=COLOR_SECUNDARIO, font=("Roboto", 15), bg=COLOR_BACKGROUND)
        self.lblConfiguracion.pack(side=tk.TOP, fill="both", expand=True)

        # --------------Etiqueta Limite-----------------------

        self.lblLimites = tk.Label(self.panel_inf, text="Limites")
        self.lblLimites.config(fg=COLOR_SECUNDARIO, font=("Roboto", 15), bg=COLOR_BACKGROUND)
        self.lblLimites.grid(row=0, column=0, padx=2, pady=1, columnspan=9)

        #--------------Tempreratura Limite-----------------------

        self.lbltemp = tk.Label(self.panel_inf, text="Limite de temperatura (C)")
        self.lbltemp.config(fg=COLOR_SECUNDARIO, font=("Roboto", 10), bg=COLOR_BACKGROUND2)
        self.lbltemp.grid(row=1, column=0, padx=2, pady=1,columnspan=3)

        self.defautl_Temp = tk.StringVar(self.panel_inf)
        self.defautl_Temp.set(f"{self.default_Values.limite_temp}")
        self.opcionesTemp = ["16","19","21","24","27","30","33","35","38","40"]
        self.menuTemp = tk.OptionMenu(self.panel_inf,self.defautl_Temp, *self.opcionesTemp)
        self.menuTemp.config(background=COLOR_BACKGROUND2,width=10)
        self.menuTemp.grid(row=2, column=0, padx=2, pady=1,columnspan=3)

        # ------------Humedad Limite-------------------------

        self.lblHum = tk.Label(self.panel_inf, text="Limite de humedad (%)")
        self.lblHum.config(fg=COLOR_SECUNDARIO, font=("Roboto", 10), bg=COLOR_BACKGROUND2)
        self.lblHum.grid(row=1, column=4, padx=2, pady=1,columnspan=3)

        self.defautl_Hum = tk.StringVar(self.panel_inf)
        self.defautl_Hum.set(f"{self.default_Values.limite_humedad}")
        self.opcionesHum = ["5","10","15","20","25","30","35","40","45","50"]
        self.menuHum = tk.OptionMenu(self.panel_inf,self.defautl_Hum, *self.opcionesHum)
        self.menuHum.config(background=COLOR_BACKGROUND2,width=10)
        self.menuHum.grid(row=2, column=4, padx=2, pady=1,columnspan=3)

        # --------------Etiqueta tiempos-----------------------

        self.lblTiempos = tk.Label(self.panel_inf, text="Tiempos de guardado")
        self.lblTiempos.config(fg=COLOR_SECUNDARIO, font=("Roboto", 15), bg=COLOR_BACKGROUND)
        self.lblTiempos.grid(row=3, column=0, padx=2, pady=1, columnspan=9)

        # -----------Intervalo Temperatura--------------------------

        self.lblItemp = tk.Label(self.panel_inf, text="Toma de Temperatura (min)")
        self.lblItemp.config(fg=COLOR_SECUNDARIO, font=("Roboto", 10), bg=COLOR_BACKGROUND2)
        self.lblItemp.grid(row=4, column=0, padx=2, pady=1,columnspan=3)

        self.defautl_ITemp = tk.StringVar(self.panel_inf)
        self.defautl_ITemp.set(f"{self.default_Values.intervalo_temp}")
        self.opcionesITemp = ["1","2","3","4","5","10","15","20","30"]
        self.menuITemp = tk.OptionMenu(self.panel_inf,self.defautl_ITemp, *self.opcionesITemp)
        self.menuITemp.config(background=COLOR_BACKGROUND2,width=10)
        self.menuITemp.grid(row=5, column=0, padx=2, pady=1,columnspan=3)

        # -----------------Intervalo Luz-------------------------

        self.lblILuz = tk.Label(self.panel_inf, text="Toma de Luz (min)")
        self.lblILuz.config(fg=COLOR_SECUNDARIO, font=("Roboto", 10), bg=COLOR_BACKGROUND2)
        self.lblILuz.grid(row=4, column=4, padx=2, pady=1,columnspan=3)

        self.defautl_ILuz = tk.StringVar(self.panel_inf)
        self.defautl_ILuz.set(f"{self.default_Values.intervalo_Luz}")
        self.opcionesILuz = ["1","2","3","4","5","10","15","20","30"]
        self.menuILuz = tk.OptionMenu(self.panel_inf,self.defautl_ILuz, *self.opcionesILuz)
        self.menuILuz.config(background=COLOR_BACKGROUND2,width=10)
        self.menuILuz.grid(row=5, column=4, padx=2, pady=1,columnspan=3)

        # -----------Intervalo Humedad Ambiente--------------------------

        self.lblIHum = tk.Label(self.panel_inf, text="Toma de Humedad" + '\n' + "de Ambiente (min)")
        self.lblIHum.config(fg=COLOR_SECUNDARIO, font=("Roboto", 10), bg=COLOR_BACKGROUND2)
        self.lblIHum.grid(row=6, column=0, padx=2, pady=1,columnspan=3)

        self.defautl_IHumA = tk.StringVar(self.panel_inf)
        self.defautl_IHumA.set(f"{self.default_Values.intervalo_humA}")
        self.opcionesIHumA = ["1","2","3","4","5","10","15","20","30"]
        self.menuIHumA = tk.OptionMenu(self.panel_inf,self.defautl_IHumA, *self.opcionesIHumA)
        self.menuIHumA.config(background=COLOR_BACKGROUND2,width=10)
        self.menuIHumA.grid(row=7, column=0, padx=2, pady=1,columnspan=3)

        # -------------Intervalo Humedad Suelo------------------------

        self.lblIHumS = tk.Label(self.panel_inf, text="Toma de Humedad" + '\n' + "de Suelo (min)")
        self.lblIHumS.config(fg=COLOR_SECUNDARIO, font=("Roboto", 10), bg=COLOR_BACKGROUND2)
        self.lblIHumS.grid(row=6, column=4, padx=2, pady=1,columnspan=3)

        self.defautl_IHumS = tk.StringVar(self.panel_inf)
        self.defautl_IHumS.set(f"{self.default_Values.intervalo_humS}")
        self.opcionesIHumS = ["1","2","3","4","5","10","15","20","30"]
        self.menuIHumS = tk.OptionMenu(self.panel_inf,self.defautl_IHumS, *self.opcionesIHumS)
        self.menuIHumS.config(background=COLOR_BACKGROUND2,width=10)
        self.menuIHumS.grid(row=7, column=4, padx=2, pady=1,columnspan=3)

        # ---------------------Intervalo abono----------------------------

        self.lblAbono = tk.Label(self.panel_inf, text="Tiempo de Abono (dias)")
        self.lblAbono.config(fg=COLOR_SECUNDARIO, font=("Roboto", 10), bg=COLOR_BACKGROUND)
        self.lblAbono.grid(row=8, column=0, padx=2, pady=1, columnspan=6)

        self.defautl_Abono = tk.StringVar(self.panel_inf)
        self.defautl_Abono.set(f"{self.default_Values.intervalo_dias_abono}")
        self.opcionesAbono = ["1","2","3","5","7","10","15","20","30","60"]
        self.menuAbono = tk.OptionMenu(self.panel_inf,self.defautl_Abono, *self.opcionesAbono)
        self.menuAbono.config(background=COLOR_BACKGROUND2,width=10)
        self.menuAbono.grid(row=9, column=1, padx=2, pady=1,columnspan=4)

        # ---------------Horas de Riego--------------------------

        self.lblHriego = tk.Label(self.panel_inf, text="Horas de Riego")
        self.lblHriego.config(fg=COLOR_SECUNDARIO, font=("Roboto", 10), bg=COLOR_BACKGROUND2)
        self.lblHriego.grid(row=10, column=0, padx=2, pady=1,columnspan=3)

        self.lblHora = tk.Label(self.panel_inf, text="Hora")
        self.lblHora.config(fg=COLOR_SECUNDARIO, font=("Roboto", 10), bg=COLOR_BACKGROUND2)
        self.lblHora.grid(row=11, column=0, padx=2, pady=1)

        self.lblMin = tk.Label(self.panel_inf, text="Min")
        self.lblMin.config(fg=COLOR_SECUNDARIO, font=("Roboto", 10), bg=COLOR_BACKGROUND2)
        self.lblMin.grid(row=11, column=2, padx=2, pady=1)

        # -------------Intervalo Hora 1------------------------

        self.defautl_H1 = tk.StringVar(self.panel_inf)
        self.defautl_H1.set(f"{self.default_Values.hora_riego[0][0]}")
        self.opcionesH1 = ["00","01","02","03","04","05","06","07","08","09","10","11","12","13","14","15","16","17","18","19","20","21","22","23","24"]
        self.menuH1 = tk.OptionMenu(self.panel_inf,self.defautl_H1, *self.opcionesH1)
        self.menuH1.config(background=COLOR_BACKGROUND2,width=2)
        self.menuH1.grid(row=12, column=0, pady=1)

        self.puntos = tk.Label(self.panel_inf, text=":")
        self.puntos.config(fg=COLOR_SECUNDARIO, font=("Roboto", 12), bg=COLOR_BACKGROUND)
        self.puntos.grid(row=12, column=1, pady=1)

        self.defautl_M1 = tk.StringVar(self.panel_inf)
        self.defautl_M1.set(f"{self.default_Values.hora_riego[0][1]}")
        self.opcionesM1 = ["00","05","10","15","20","25","30","35","40","45","50","55"]
        self.menuM1 = tk.OptionMenu(self.panel_inf,self.defautl_M1, *self.opcionesM1)
        self.menuM1.config(background=COLOR_BACKGROUND2,width=2)
        self.menuM1.grid(row=12, column=2, pady=1)

        # -------------Intervalo Hora 2------------------------

        self.defautl_H2 = tk.StringVar(self.panel_inf)
        self.defautl_H2.set(f"{self.default_Values.hora_riego[1][0]}")
        self.opcionesH2 = ["00","01","02","03","04","05","06","07","08","09","10","11","12","13","14","15","16","17","18","19","20","21","22","23","24"]
        self.menuH2 = tk.OptionMenu(self.panel_inf,self.defautl_H2, *self.opcionesH2)
        self.menuH2.config(background=COLOR_BACKGROUND2,width=2)
        self.menuH2.grid(row=13, column=0, pady=1)

        self.puntos2 = tk.Label(self.panel_inf, text=":")
        self.puntos2.config(fg=COLOR_SECUNDARIO, font=("Roboto", 12), bg=COLOR_BACKGROUND)
        self.puntos2.grid(row=13, column=1, pady=1)

        self.defautl_M2 = tk.StringVar(self.panel_inf)
        self.defautl_M2.set(f"{self.default_Values.hora_riego[1][1]}")
        self.opcionesM2 = ["00","05","10","15","20","25","30","35","40","45","50","55"]
        self.menuM2 = tk.OptionMenu(self.panel_inf,self.defautl_M2, *self.opcionesM2)
        self.menuM2.config(background=COLOR_BACKGROUND2,width=2)
        self.menuM2.grid(row=13, column=2, pady=1)


        self.btnAplicar = tk.Button(self.panel_inf,text="Aplicar")
        self.btnAplicar.config(background=COLOR_BACKGROUND2,width=15,command=self.aplicar_Cambios)
        self.btnAplicar.grid(row=14, column=3, pady=5,padx=5,columnspan=4)

    def aplicar_Cambios(self):
        self.default_Values.limite_temp = int(self.defautl_Temp.get())
        self.default_Values.limite_humedad = int(self.defautl_Hum.get())
        self.default_Values.intervalo_temp = int(self.defautl_ITemp.get())
        self.default_Values.intervalo_Luz = int(self.defautl_ILuz.get())
        self.default_Values.intervalo_humA = int(self.defautl_IHumA.get())
        self.default_Values.intervalo_humS = int(self.defautl_IHumS.get())
        self.default_Values.intervalo_dias_abono = int(self.defautl_Abono.get())
        self.default_Values.hora_riego[0][0] = int(self.defautl_H1.get())
        self.default_Values.hora_riego[0][1] = int(self.defautl_M1.get())
        self.default_Values.hora_riego[1][0] = int(self.defautl_H2.get())
        self.default_Values.hora_riego[1][1] = int(self.defautl_M2.get())
        self.default_Values.guardar_config()

