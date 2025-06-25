import json
import os
import time
import datetime as dt
from DB.Defaut_Values import default_Values
import cv2

ARCHIVO_ABONO = "./DB/Archivos/abono_config.json"
class Gestor_automatico():

    def __init__(self):
        self.ultima_ejecucion_riego = None

    def verificar_recordatorio_abono(self) -> bool:

        try:
            with open(ARCHIVO_ABONO, "r") as f:
                data = json.load(f)

            abono = data.get(default_Values().codigo)

            if not abono:
                return False  # No config
            ultima = dt.datetime.strptime(abono["ultimo_abono"], "%Y-%m-%d")
            intervalo = abono.get("intervalo_abono", default_Values().intervalo_dias_abono)
            hoy = dt.datetime.now().date()
            return hoy >= (ultima + dt.timedelta(days=intervalo)).date()

        except Exception as e:
            return False

    def registrar_aplicacion_abono(self):
        try:
            with open(ARCHIVO_ABONO, "r") as f:
                data = json.load(f)
        except FileNotFoundError:
            data = {}

        if default_Values().codigo not in data:
            data[default_Values().codigo] = {
                "intervalo_abono": default_Values().intervalo_dias_abono,
                "ultima_abono": dt.datetime.now().strftime("%Y-%m-%d")
            }
        else:
            data[default_Values().codigo]["ultima_abono"] = dt.datetime.now().strftime("%Y-%m-%d")

        with open(ARCHIVO_ABONO, "w") as f:
            json.dump(data, f, indent=4)

    def verificar_riego(self, nivel_humedad, nivel_agua, arduino):
        ahora = dt.datetime.now()
        hora = ahora.hour
        minuto = ahora.minute

        if nivel_agua > 15:
            # Riego automático por humedad baja
            if nivel_humedad < default_Values().limite_humedad:
                self.ciclo_riego(arduino)

            # Riego programado por horario
            for hora_riego_info in default_Values().hora_riego:
                hora_riego = hora_riego_info[0]
                minuto_riego = hora_riego_info[1]

                if hora == hora_riego and minuto == minuto_riego:
                    # Evita repetir si ya se regó en este minuto
                    if self.ultima_ejecucion_riego != (hora, minuto):
                        self.ciclo_riego(arduino)
                        self.ultima_ejecucion_riego = (hora, minuto)

    def ciclo_riego(self,arduino):

        arduino.enviar_comando("riego", True)
        time.sleep(10)
        arduino.enviar_comando("riego", False)

    def verificar_foto(self,ultima_foto):
        ahora = dt.datetime.now()
        if ultima_foto is None or (ahora - ultima_foto).total_seconds() >= default_Values().intervalo_Cam * 60:
            ret, frame = default_Values().cap.read()
            if ret:
                nombre = ahora.strftime("%Y-%m-%d_%H-%M-%S") + ".jpg"
                ruta_completa = os.path.join(default_Values().CARPETA_FOTOS, nombre)
                cv2.imwrite(ruta_completa, frame)
                return ahora

            else:
                return ultima_foto
        return ultima_foto

    def tomar_foto(self):
        ahora = dt.datetime.now()

        ret, frame = default_Values().cap.read()
        if ret:
            nombre = ahora.strftime("%Y-%m-%d_%H-%M-%S") + ".jpg"
            ruta_completa = os.path.join(default_Values().CARPETA_FOTOS, nombre)
            cv2.imwrite(ruta_completa, frame)
            default_Values().ultima_foto = ahora

