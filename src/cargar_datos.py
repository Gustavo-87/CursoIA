import csv


def leer_datos(ruta_archivo):
    datos = []

    with open(ruta_archivo, mode="r", encoding="utf-8") as archivo:
        lector = csv.DictReader(archivo)

        for fila in lector:
            fila["dias_abierta"] = int(fila["dias_abierta"])
            datos.append(fila)

    return datos


def mostrar_resumen(datos):
    dias = [pqrs["dias_abierta"] for pqrs in datos]

    promedio = sum(dias) / len(dias)
    maximo = max(dias)
    minimo = min(dias)

    print("Cantidad total de registros:", len(datos))
    print("Promedio de días abiertos:", promedio)
    print("Máximo de días abiertos:", maximo)
    print("Mínimo de días abiertos:", minimo)


datos_pqrs = leer_datos("data/pqrs/pqrs.csv")

mostrar_resumen(datos_pqrs)
