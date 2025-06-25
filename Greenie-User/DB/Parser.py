import csv
import os
import threading
import time
import traceback
from datetime import datetime, timedelta

from DB.Defaut_Values import default_Values
from DB.gestor_automatico import Gestor_automatico

class Parser(threading.Thread):
    def __init__(self, arduino):
        super().__init__()
        self.arduino = arduino
        self.running = True

    def run(self):
        gestor = Gestor_automatico()
        self.obtener_ultimasLecturas()
        default_Values().ultima_Foto = self.obtener_ultimafoto()
        while self.running:
            try:
                datos = self.arduino.obtener_datos()
                if datos:

                    sensores = [
                        ("temp", "temperatura", default_Values().archivo_Temp, default_Values().intervalo_temp,default_Values().ultima_temp),
                        ("humA", "humedadAmbiente", default_Values().archivo_humA, default_Values().intervalo_humA,default_Values().ultima_HumA),
                        ("humS", "humedadSuelo", default_Values().archivo_humS, default_Values().intervalo_humS,default_Values().ultima_HumS),
                        ("luzA", "luzAmbiente", default_Values().archivo_Luz, default_Values().intervalo_Luz,default_Values().ultima_LuzA)
                    ]

                    for sensor_id, clave_dato, archivo, intervalo, ultima in sensores:
                        valor = datos.get(clave_dato)
                        if valor not in (None, "--"):
                            self.guardar_lectura(archivo, valor, intervalo, sensor_id, ultima)

                    gestor.verificar_riego(
                        datos.get("humedadSuelo", "--"),
                        datos.get("aguaPotable", "--"),
                        self.arduino
                    )
                    default_Values().notificacion_abono = gestor.verificar_recordatorio_abono()

                    default_Values().ultima_Foto = gestor.verificar_foto(default_Values().ultima_Foto)

                    if datos.get("aguaPotable", "--") < 20:
                        default_Values().notificacion_agua = True
                    else:
                        default_Values().notificacion_agua = False

                    if datos.get("aguaDrenada", "--") > 80:
                        default_Values().notificacion_drenaje = True
                    else:
                        default_Values().notificacion_drenaje = False

                time.sleep(0.5)
            except Exception as e:
                print(f"[Parser] Error: {e}")
                traceback.print_exc()
                time.sleep(1)

    def obtener_ultimafoto(self):
        archivos = [f for f in os.listdir(default_Values().CARPETA_FOTOS) if f.lower().endswith(default_Values().EXTENSION)]
        if not archivos:
            return None  # No hay fotos aún

        fechas = []
        for archivo in archivos:
            nombre_sin_ext = os.path.splitext(archivo)[0]
            try:
                # Convierte nombre a datetime, formato: 2025-06-24_17-42-10
                fecha = datetime.strptime(nombre_sin_ext, "%Y-%m-%d_%H-%M-%S")
                fechas.append(fecha)
            except ValueError:
                # Ignorar archivos que no cumplan el formato esperado
                pass

        if not fechas:
            return None  # No había archivos con formato válido

        return max(fechas)  # Fecha más reciente

    def obtener_ultimasLecturas(self):
        archivos = [
            default_Values().archivo_Temp,
            default_Values().archivo_humA,
            default_Values().archivo_humS,
            default_Values().archivo_Luz,
        ]
        for nombre_archivo in archivos:
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
        return None

    def guardar_lectura(self, nombre_archivo, dato, intervalo, sensor,ultima_lectura):
        ahora = datetime.now()
        if not ultima_lectura or (ahora - ultima_lectura >= timedelta(seconds=intervalo)):
            archivo_nuevo = not os.path.exists(nombre_archivo)
            with open(nombre_archivo, mode='a', newline='', encoding='utf-8') as archivo:
                escritor = csv.writer(archivo)
                encabezado = ['Fecha', 'Hora', 'dato']
                fila = [ahora.strftime('%Y-%m-%d'), ahora.strftime('%H:%M:%S'), dato]

                if sensor == 'temp':
                    encabezado.append('Compuerta')
                    fila.append(default_Values().compuerta)

                if archivo_nuevo:
                    escritor.writerow(encabezado)
                escritor.writerow(fila)
            self.obtener_ultimasLecturas()

    def detener(self):
        self.running = False