import json

try:
    with open("datos.json", "r", encoding="utf-8") as archivo:
        datos = json.load(archivo)

    print(datos)

except FileNotFoundError:
    print("Archivo no encontrado.")

except json.JSONDecodeError:
    print("El archivo no tiene un formato JSON válido.")