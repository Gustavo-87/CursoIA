import json

nuevos_datos = [
    {"nombre": "Cacao", "hectareas": 8, "produccion_toneladas": 3.5},
    {"nombre": "Palma", "hectareas": 12, "produccion_toneladas": 7.2}
]

with open("nuevos_cultivos.json", "w", encoding="utf-8") as archivo:
    json.dump(nuevos_datos, archivo, indent=4, ensure_ascii=False)