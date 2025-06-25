import json
from datetime import datetime, timedelta

ARCHIVO_ABONO = "gestor_abono/abono_config.json"

def verificar_recordatorio_abono(codigo: str) -> bool:
    try:
        with open(ARCHIVO_ABONO, "r") as f:
            data = json.load(f)

        abono = data.get(codigo)
        if not abono:
            return False  # No config

        ultima = datetime.strptime(abono["ultima_aplicacion"], "%Y-%m-%d")
        intervalo = abono.get("intervalo_dias", 7)
        hoy = datetime.now().date()

        return hoy >= (ultima + timedelta(days=intervalo)).date()

    except Exception as e:
        print(f"[Error] abono: {e}")
        return False

def registrar_aplicacion_abono(codigo: str):
    try:
        with open(ARCHIVO_ABONO, "r") as f:
            data = json.load(f)
    except FileNotFoundError:
        data = {}

    if codigo not in data:
        data[codigo] = {
            "intervalo_dias": 7,
            "ultima_aplicacion": datetime.now().strftime("%Y-%m-%d")
        }
    else:
        data[codigo]["ultima_aplicacion"] = datetime.now().strftime("%Y-%m-%d")

    with open(ARCHIVO_ABONO, "w") as f:
        json.dump(data, f, indent=4)
