cultivos = [
    {"nombre": "Café", "hectareas": 5, "produccion_toneladas": 3.2},
    {"nombre": "Caña", "hectareas": 10, "produccion_toneladas": 8.5},
]

region = {
    "nombre": "Cartago",
    "cultivos": ["Café", "Caña", "Maíz"],
    "produccion": [3.2, 8.5, 1.8],
}

print(cultivos[0]["nombre"])
print(region["cultivos"][0])
print(region["produccion"][1])