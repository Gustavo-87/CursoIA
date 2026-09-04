import csv

with open("cultivos.csv", "r", encoding="utf-8") as archivo:
    lector = csv.DictReader(archivo)

    for fila in lector:
        print(fila)
        