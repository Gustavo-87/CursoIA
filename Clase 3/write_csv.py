import csv

with open("nuevos_cultivos.csv", "w", newline="", encoding="utf-8") as archivo:
    escritor = csv.writer(archivo)
    escritor.writerow(["nombre", "hectareas", "produccion_toneladas"])
    escritor.writerow(["Cacao", 8, 3.5])
    escritor.writerow(["Palma", 12, 7.2])