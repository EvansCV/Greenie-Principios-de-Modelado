import json
import threading
import time
import serial

class ArduinoThread(threading.Thread):
    def __init__(self, puerto='COM3', baudios=9600):
        super().__init__()
        self.puerto = puerto
        self.baudios = baudios
        self.arduino = None
        self.running = True
        self.datos = {}
        self.estado = False
        self.labelEstado = "Desconectado"
        self.lock = threading.Lock()

    def conectar(self):
        while self.running:
            try:
                self.labelEstado = "Intentando conectar..."
                self.arduino = serial.Serial(self.puerto, self.baudios, timeout=1)
                time.sleep(2)  # espera inicial por seguridad
                self.estado = True
                self.labelEstado = "Conectado"
                return
            except serial.SerialException:
                self.estado = False
                self.labelEstado = "Desconectado"
                time.sleep(1)  # reconexión más rápida

    def enviar_comando(self, sistema, comando):
        if self.arduino and self.arduino.is_open and self.estado:
            try:
                mensaje = {sistema: comando}
                json_str = json.dumps(mensaje) + "\n"
                self.arduino.write(json_str.encode())
            except Exception as e:
                print(f"⚠️ Error al enviar comando: {e}")

    def leer_datos(self):
        if self.arduino and self.arduino.in_waiting:
            linea = self.arduino.readline().decode('utf-8').strip()
            try:
                data = json.loads(linea)
                with self.lock:
                    self.datos = data
            except json.JSONDecodeError:
                print("⚠️ JSON inválido:", linea)

    def run(self):
        self.conectar()
        while self.running:
            try:
                if self.arduino:
                    linea = self.arduino.readline().decode('utf-8').strip()
                    if linea:
                        try:
                            data = json.loads(linea)
                            with self.lock:
                                self.datos = data
                        except json.JSONDecodeError:
                            print("⚠️ JSON inválido:", linea)
            except serial.SerialException:
                print("🔌 Desconectado. Reintentando conexión...")
                self.estado = False
                self.labelEstado = "Reconectando..."
                try:
                    self.arduino.close()
                except:
                    pass
                self.conectar()
            except Exception as e:
                print("⚠️ Error inesperado:", e)
            time.sleep(0.01)  # ciclo ágil sin saturar CPU

    def obtener_datos(self):
        with self.lock:
            return self.datos.copy()

    def obtener_estado(self):
        with self.lock:
            return self.estado

    def detener(self):
        self.running = False
        if self.arduino:
            try:
                self.arduino.close()
            except:
                pass
