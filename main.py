from gestor_abono.gestor_abono import verificar_recordatorio_abono, registrar_aplicacion_abono
from gestor_graficas.gestor_graficas import graficar_variable

codigo = "ABC123"

# US25: verificar si se debe abonar hoy
if verificar_recordatorio_abono(codigo):
    print("Recordatorio: ¡Hora de agregar abono!")
    registrar_aplicacion_abono(codigo)
else:
    print("Aún no es necesario abonar.")

# US12: graficar humedad
graficar_variable(codigo, "humedad")
