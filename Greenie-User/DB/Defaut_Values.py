import datetime
import json
import os

class default_Values():

    _instancia = None

    def __new__(cls):
        if cls._instancia is None:
            cls._instancia = super(default_Values, cls).__new__(cls)
        return cls._instancia

    def __init__(self):
        # Solo inicializar una vez
        if hasattr(self, '_inicializado') and self._inicializado:
            return
        self._inicializado = True

        self.codigo = " "

        self.intervalo_temp = 60
        self.intervalo_humS = 90
        self.intervalo_humA = 90
        self.intervalo_Luz = 60
        self.compuerta = False

        self.limite_humedad = 10
        self.limite_temp = 26

        self.hora_riego = [[22,15],[0,0]]
        self.intervalo_dias_abono = 7

        self.archivo_Temp = "./DB/Archivos/dataTemp.csv"
        self.archivo_humS = "./DB/Archivos/datahumS.csv"
        self.archivo_humA = "./DB/Archivos/datahumA.csv"
        self.archivo_Luz = "./DB/Archivos/dataLuz.csv"
        self.ruta_config = "./DB/Archivos/config.json"

        self.notificacion_abono = True

    def cargar_config(self):
        if not os.path.exists(self.ruta_config):
            datos = {
                "intervalo_temp": self.intervalo_temp,
                "intervalo_humS": self.intervalo_humS,
                "intervalo_humA": self.intervalo_humA,
                "intervalo_Luz": self.intervalo_Luz,
                "hora_riego": self.hora_riego,
                "limite_temp": self.limite_temp,
                "limite_humedad": self.limite_humedad,
                "intervalo_dias_abono": self.intervalo_dias_abono
            }

            with open(self.ruta_config, 'w', encoding='utf-8') as archivo:
                json.dump(datos, archivo, indent=4)

        with open(self.ruta_config, 'r', encoding='utf-8') as archivo:
            datos = json.load(archivo)
            self.intervalo_temp = datos.get("intervalo_temp", self.intervalo_temp)
            self.intervalo_humS = datos.get("intervalo_humS", self.intervalo_humS)
            self.intervalo_humA = datos.get("intervalo_humA", self.intervalo_humA)
            self.intervalo_Luz = datos.get("intervalo_Luz", self.intervalo_Luz)
            self.hora_riego = datos.get("hora_riego", self.hora_riego)
            self.limite_temp = datos.get("limite_temp", self.limite_temp)
            self.limite_humedad = datos.get("limite_humedad",self.limite_humedad)
            self.intervalo_dias_abono = datos.get("intervalo_dias_abono", self.intervalo_dias_abono)

    def guardar_config(self):
        datos = {
            "intervalo_temp": self.intervalo_temp,
            "intervalo_humS": self.intervalo_humS,
            "intervalo_humA": self.intervalo_humA,
            "intervalo_Luz": self.intervalo_Luz,
            "hora_riego": self.hora_riego,
            "limite_temp": self.limite_temp,
            "limite_humedad": self.limite_humedad,
            "intervalo_dias_abono": self.intervalo_dias_abono
        }

        with open(self.ruta_config, 'w', encoding='utf-8') as archivo:
            json.dump(datos, archivo, indent=4)

