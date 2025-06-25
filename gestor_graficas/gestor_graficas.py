import json
import matplotlib.pyplot as plt
from datetime import datetime

HISTORIAL_FILE = "gestor_graficas/historial_sensores.json"

def graficar_variable(codigo: str, variable: str):
    try:
        with open(HISTORIAL_FILE, "r") as f:
            data = json.load(f)

        registros = data.get(codigo, {}).get(variable, [])
        if not registros:
            print("No hay datos disponibles.")
            return

        fechas = [datetime.strptime(p["fecha"], "%Y-%m-%d") for p in registros]
        valores = [p["valor"] for p in registros]

        plt.figure(figsize=(8, 4))
        plt.plot(fechas, valores, marker='o', linestyle='-', color='green')
        plt.title(f"{variable.capitalize()} a lo largo del tiempo")
        plt.xlabel("Fecha")
        plt.ylabel("Valor")
        plt.grid(True)
        plt.tight_layout()
        plt.show()

    except Exception as e:
        print(f"[Error] al graficar: {e}")
