
import joblib
import pandas as pd

# 1. Cargar el modelo entrenado
modelo = joblib.load("clase12/modelo_pqrs.joblib")

# 2. Crear tres casos nuevos de PQRS
nuevas_pqrs = pd.DataFrame({
    "dias_abierta": [5, 25, 55],
    "cantidad_adjuntos": [1, 3, 5]
})

# 3. Realizar predicciones
predicciones = modelo.predict(nuevas_pqrs)

# 4. Calcular probabilidades
probabilidades = modelo.predict_proba(nuevas_pqrs)[:, 1]

# 5. Mostrar resultados
nuevas_pqrs["probabilidad_cierre_%"] = (
    probabilidades * 100
).round(1)

nuevas_pqrs["prediccion"] = [
    "Cerrada" if p == 1 else "No cerrada"
    for p in predicciones
]

print("Predicciones de nuevas PQRS:")
print(nuevas_pqrs.to_string(index=False))
