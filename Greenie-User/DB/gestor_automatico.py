import json
import time
import datetime as dt
from DB.Defaut_Values import default_Values

ARCHIVO_ABONO = "./DB/Archivos/abono_config.json"
class Gestor_automatico():

    TempAlta = 0
    TempBaja = 0
    statusvent = False

    def __init__(self):
        self.ultima_ejecucion_riego = None

    def verificar_recordatorio_abono(self) -> bool:
        try:
            with open(ARCHIVO_ABONO, "r") as f:
                data = json.load(f)

            abono = data.get(default_Values().codigo)
            if not abono:
                return False  # No config

            ultima = dt.datetime.strptime(abono["ultima_abono"], "%Y-%m-%d")
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

    def verificar_temp(self, limite_temp, temp, arduino):
        if limite_temp < temp:
            Gestor_automatico.TempAlta += 1
            Gestor_automatico.TempBaja = 0
            if Gestor_automatico.TempAlta >= 15 and not Gestor_automatico.statusvent:
                arduino.enviar_comando("vent", True)
                Gestor_automatico.statusvent = True
        else:
            Gestor_automatico.TempBaja += 1
            Gestor_automatico.TempAlta = 0
            if Gestor_automatico.TempBaja >= 15 and not Gestor_automatico.statusvent:
                arduino.enviar_comando("vent", False)
                Gestor_automatico.statusvent = False