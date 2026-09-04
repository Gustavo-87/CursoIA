import json

with open("cultivos.json", "r", encoding="utf-8") as archivo:
    datos = json.load(archivo)

for cultivo in datos:
    print(cultivo["nombre"], cultivo["hectareas"])