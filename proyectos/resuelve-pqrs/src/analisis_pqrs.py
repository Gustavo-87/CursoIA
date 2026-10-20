import csv

import matplotlib.pyplot as plt
import numpy as np


def cargar_pqrs():
    """Carga el archivo CSV como una lista de diccionarios."""
    datos = []

    with open("data/pqrs.csv", "r", encoding="utf-8") as archivo:
        lector = csv.DictReader(archivo)

        for fila in lector:
            fila["dias_desde_radicacion"] = int(
                fila["dias_desde_radicacion"]
            )
            datos.append(fila)

    return datos


pqrs = cargar_pqrs()

dias = np.array(
    [pqr["dias_desde_radicacion"] for pqr in pqrs]
)

print("Cantidad de registros:", len(pqrs))
print("Promedio de días:", round(np.mean(dias), 2))
print("Máximo de días:", np.max(dias))
print("Mínimo de días:", np.min(dias))
print("Desviación estándar:", round(np.std(dias), 2))

conteo_tipos = {}

for pqr in pqrs:
    tipo = pqr["tipo"]
    conteo_tipos[tipo] = conteo_tipos.get(tipo, 0) + 1

plt.bar(conteo_tipos.keys(), conteo_tipos.values())
plt.title("Cantidad de PQRS por tipo")
plt.xlabel("Tipo de PQRS")
plt.ylabel("Cantidad")
plt.tight_layout()
plt.savefig("grafico_pqrs.png")
plt.show()

tipo_mas_frecuente = max(conteo_tipos, key=conteo_tipos.get)

pendientes = 0

for pqr in pqrs:
    if pqr["estado"] in ["Radicada", "En revisión"]:
        pendientes += 1

porcentaje_pendientes = pendientes / len(pqrs) * 100

print("\nHallazgos:")
print(
    "1. El tipo más frecuente es",
    tipo_mas_frecuente,
    "con",
    conteo_tipos[tipo_mas_frecuente],
    "registros.",
)
print(
    "2. El",
    round(porcentaje_pendientes, 1),
    "% de las PQRS está radicado o en revisión.",
)