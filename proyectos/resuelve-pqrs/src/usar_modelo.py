
from pathlib import Path

import joblib
import pandas as pd

BASE_DIR = Path(__file__).resolve().parents[1]

# 1. Cargar el modelo guardado sin volver a entrenarlo
modelo = joblib.load(BASE_DIR / "modelo_pqrs_final.joblib")

# 2. Crear tres PQRS nuevas con datos simulados
nuevas_pqrs = pd.DataFrame({
    "dias_desde_radicacion": [5, 45, 120],
    "longitud_descripcion": [90, 65, 75],
    "cantidad_adjuntos": [1, 3, 5],
    "tipo": ["Petición", "Queja", "Reclamo"]
})

# 3. Predecir prioridad alta (0 o 1)
predicciones = modelo.predict(nuevas_pqrs)
probabilidades = modelo.predict_proba(nuevas_pqrs)[:, 1]

# 4. Mostrar los resultados
nuevas_pqrs["probabilidad_prioridad_alta_%"] = (
    probabilidades * 100
).round(1)

nuevas_pqrs["prioridad_predicha"] = [
    "Alta" if valor == 1 else "No alta"
    for valor in predicciones
]

print("Predicciones de prioridad de PQRS:")
print(nuevas_pqrs.to_string(index=False))
