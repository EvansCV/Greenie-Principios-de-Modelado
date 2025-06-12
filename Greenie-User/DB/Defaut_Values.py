import datetime
import json
import os
class default_Values():

    _instancia = None

    codigo = " "

    intervalo_temp = 60
    intervalo_humS = 90
    intervalo_humA = 90
    intervalo_Luz = 60
    compuerta = False

    limite_humedad = 10
    limite_temp = 26

    hora_riego = [[22,15],[0,0]]
    intervalo_dias_abono = 7

    archivo_Temp = "./DB/Archivos/dataTemp.csv"
    archivo_humS = "./DB/Archivos/datahumS.csv"
    archivo_humA = "./DB/Archivos/datahumA.csv"
    archivo_Luz = "./DB/Archivos/dataLuz.csv"
    ruta_config = "./DB/Archivos/config.json"

    notificacion_abono = False

    def __new__(cls):
        if cls._instancia is None:
            cls._instancia = super(default_Values, cls).__new__(cls)
        return cls._instancia

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

    def guardar_config(self):
        datos = {
            "intervalo_temp": self.intervalo_temp,
            "intervalo_humS": self.intervalo_humS,
            "intervalo_humA": self.intervalo_humA,
            "intervalo_Luz": self.intervalo_Luz,
            "hora_riego": self.hora_riego,
            "limite_temp": self.limite_temp,
            "limite_humedad": self.limite_humedad,
        }

        with open(self.ruta_config, 'w', encoding='utf-8') as archivo:
            json.dump(datos, archivo, indent=4)

