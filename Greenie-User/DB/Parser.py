import csv
import os
import threading
import time
from datetime import datetime, timedelta
from DB.Defaut_Values import default_Values
from DB.gestor_automatico import Gestor_automatico

class Parser(threading.Thread):
    def __init__(self, arduino):
        super().__init__()
        self.arduino = arduino
        self.running = True
        self.default_Values = default_Values()

    def run(self):
        gestor = Gestor_automatico()
        while self.running:
            try:
                datos = self.arduino.obtener_datos()
                if datos:

                    sensores = [
                        ("temp", "temperatura", self.default_Values.archivo_Temp, self.default_Values.intervalo_temp),
                        ("humA", "humedadAmbiente", self.default_Values.archivo_humA, self.default_Values.intervalo_humA),
                        ("humS", "humedadSuelo", self.default_Values.archivo_humS, self.default_Values.intervalo_humS),
                        ("luzA", "luzAmbiente", self.default_Values.archivo_Luz, self.default_Values.intervalo_Luz)
                    ]

                    for sensor_id, clave_dato, archivo, intervalo in sensores:
                        valor = datos.get(clave_dato)
                        if valor not in (None, "--"):
                            self.guardar_lectura(archivo, valor, intervalo, sensor_id)

                    gestor.verificar_riego(
                        datos.get("humedadSuelo", "--"),
                        datos.get("aguaPotable", "--"),
                        self.arduino
                    )
                    default_Values.notificacion_abono = gestor.verificar_recordatorio_abono()

                    gestor.verificar_temp(
                        self.default_Values.limite_temp,
                        datos.get("temperatura", "--"),
                        self.arduino
                    )


                time.sleep(0.5)
            except Exception as e:
                time.sleep(1)


    def obtener_ultima_fecha_hora(self, nombre_archivo):
        if not os.path.exists(nombre_archivo):
            return None
        with open(nombre_archivo, mode='r', encoding='utf-8') as archivo:
            lineas = list(csv.reader(archivo))
            if len(lineas) <= 1:
                return None
            ultima = lineas[-1]
            try:
                fecha_hora = datetime.strptime(f"{ultima[0]} {ultima[1]}", '%Y-%m-%d %H:%M:%S')
                return fecha_hora
            except Exception:
                return None

    def guardar_lectura(self, nombre_archivo, dato, intervalo, sensor):
        ahora = datetime.now()
        ultima_lectura = self.obtener_ultima_fecha_hora(nombre_archivo)
        if not ultima_lectura or (ahora - ultima_lectura >= timedelta(seconds=intervalo)):
            archivo_nuevo = not os.path.exists(nombre_archivo)
            with open(nombre_archivo, mode='a', newline='', encoding='utf-8') as archivo:
                escritor = csv.writer(archivo)
                encabezado = ['Fecha', 'Hora', 'dato']
                fila = [ahora.strftime('%Y-%m-%d'), ahora.strftime('%H:%M:%S'), dato]

                if sensor == 'temp':
                    encabezado.append('Compuerta')
                    fila.append(self.default_Values.compuerta)

                if archivo_nuevo:
                    escritor.writerow(encabezado)
                escritor.writerow(fila)

    def detener(self):
        self.running = False