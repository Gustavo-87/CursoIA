import csv
import json

import matplotlib.pyplot as plt
import numpy as np


RUTA_CSV = "data/pqrs/pqrs.csv"


def cargar_datos(ruta_archivo):
    dias_abierta = []
    cantidad_adjuntos = []

    with open(ruta_archivo, mode="r", encoding="utf-8") as archivo:
        lector = csv.DictReader(archivo)

        for fila in lector:
            dias_abierta.append(int(fila["dias_abierta"]))
            cantidad_adjuntos.append(int(fila["cantidad_adjuntos"]))

    return (
        np.array(dias_abierta),
        np.array(cantidad_adjuntos),
    )


def calcular_estadisticas(datos):
    return {
        "media": float(np.mean(datos)),
        "mediana": float(np.median(datos)),
        "desviacion_estandar": float(np.std(datos)),
        "minimo": float(np.min(datos)),
        "maximo": float(np.max(datos)),
    }


def generar_histograma(dias_abierta):
    plt.figure()

    plt.hist(dias_abierta, bins=5)

    plt.title("Distribución de días abiertos de las PQRS")
    plt.xlabel("Días abierta")
    plt.ylabel("Frecuencia")

    plt.savefig(
        "data/eda/histograma_dias_abierta.png",
        dpi=150,
        bbox_inches="tight",
    )

    plt.close()


def generar_dispersion(dias_abierta, cantidad_adjuntos):
    plt.figure()

    plt.scatter(cantidad_adjuntos, dias_abierta)

    plt.title("Relación entre adjuntos y días abiertos")
    plt.xlabel("Cantidad de adjuntos")
    plt.ylabel("Días abierta")

    plt.savefig(
        "data/eda/dias_vs_adjuntos.png",
        dpi=150,
        bbox_inches="tight",
    )

    plt.close()


def guardar_estadisticas(estadisticas):
    with open("data/eda/estadisticas.txt", mode="w", encoding="utf-8") as archivo:
        json.dump(
            estadisticas,
            archivo,
            indent=4,
            ensure_ascii=False,
        )


def main():
    dias_abierta, cantidad_adjuntos = cargar_datos(RUTA_CSV)

    estadisticas = {
        "dias_abierta": calcular_estadisticas(dias_abierta),
        "cantidad_adjuntos": calcular_estadisticas(cantidad_adjuntos),
    }

    print("ANÁLISIS EXPLORATORIO DE DATOS - RESUELVE")
    print()

    for variable, resultados in estadisticas.items():
        print(variable)

        for nombre, valor in resultados.items():
            print(f"  {nombre}: {valor:.2f}")

        print()

    generar_histograma(dias_abierta)
    generar_dispersion(dias_abierta, cantidad_adjuntos)
    guardar_estadisticas(estadisticas)

    print("Archivos generados:")
    print("- data/eda/histograma_dias_abierta.png")
    print("- data/eda/dias_vs_adjuntos.png")
    print("- data/eda/estadisticas.txt")


if __name__ == "__main__":
    main()