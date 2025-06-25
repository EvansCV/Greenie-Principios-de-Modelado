import json

USUARIOS_FILE = "gestor_config/usuarios.json"
CONFIG_FILE = "gestor_config/configuraciones.json"

def verificar_credenciales(codigo_dispositivo: str, password: str) -> bool:
    try:
        with open(USUARIOS_FILE, "r") as f:
            data = json.load(f)
        return codigo_dispositivo in data and data[codigo_dispositivo]["password"] == password
    except Exception as e:
        print(f"[Error] al verificar credenciales: {e}")
        return False

def cargar_configuracion_por_defecto_si_aplica(codigo_dispositivo: str) -> bool:
    try:
        with open(USUARIOS_FILE, "r") as f:
            usuarios = json.load(f)

        if usuarios.get(codigo_dispositivo, {}).get("es_nuevo", False):
            with open(CONFIG_FILE, "r") as f:
                config = json.load(f)

            if codigo_dispositivo not in config:
                config[codigo_dispositivo] = {
                    "intervalo_riego": 30,
                    "frecuencia_datos": 5,
                    "umbral_humedad": 40
                }

            usuarios[codigo_dispositivo]["es_nuevo"] = False

            with open(USUARIOS_FILE, "w") as f:
                json.dump(usuarios, f, indent=4)
            with open(CONFIG_FILE, "w") as f:
                json.dump(config, f, indent=4)

            return True
        return False
    except Exception as e:
        print(f"[Error] al cargar configuración: {e}")
        return False

def obtener_configuracion_actual(codigo_dispositivo: str) -> dict | None:
    try:
        with open(CONFIG_FILE, "r") as f:
            data = json.load(f)
        return data.get(codigo_dispositivo)
    except Exception as e:
        print(f"[Error] al leer configuración: {e}")
        return None

def modificar_configuracion_por_defecto(codigo_dispositivo: str, nuevos_valores: dict) -> bool:
    try:
        with open(CONFIG_FILE, "r") as f:
            config = json.load(f)

        if codigo_dispositivo not in config:
            print(f"[Error] Dispositivo {codigo_dispositivo} no encontrado.")
            return False

        config[codigo_dispositivo].update(nuevos_valores)

        with open(CONFIG_FILE, "w") as f:
            json.dump(config, f, indent=4)
        return True
    except Exception as e:
        print(f"[Error] al modificar configuración: {e}")
        return False
