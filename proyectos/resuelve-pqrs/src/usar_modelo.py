"""Predicción de casos nuevos con el modelo final de PQRS guardado.

Carga modelo_pqrs_final.joblib (entrenado por src/modelo_proyecto.py) y
predice casos nuevos SIN volver a entrenar.

Contrato único de variables de entrada (idéntico al entrenamiento):
    - dias_desde_radicacion (numérica)
    - longitud_descripcion  (numérica)
    - cantidad_adjuntos     (numérica)
    - tipo                  (categórica)

LIMITACIONES METODOLÓGICAS (visibles, no ocultar):
- Los datos de entrenamiento son SINTÉTICOS (src/generar_datos.py).
- CIRCULARIDAD / FUGA METODOLÓGICA: la variable objetivo prioridad_alta se
  generó a partir de las MISMAS variables de entrada; el modelo solo aprende
  esa regla artificial y sus probabilidades no son confiables en la realidad.
- Sistema ACADÉMICO, no apto para asignar prioridades reales de PQRS.
"""

from pathlib import Path

import joblib
import pandas as pd

BASE_DIR = Path(__file__).resolve().parents[1]
RUTA_MODELO = BASE_DIR / "modelo_pqrs_final.joblib"

# Contrato único de variables (idéntico al de src/modelo_proyecto.py)
COLUMNAS_ENTRADA = [
    "dias_desde_radicacion",
    "longitud_descripcion",
    "cantidad_adjuntos",
    "tipo",
]


def main():
    # 1. Cargar el modelo guardado sin volver a entrenarlo
    modelo = joblib.load(RUTA_MODELO)

    # 2. Crear casos nuevos con las mismas cuatro variables del entrenamiento
    nuevas_pqrs = pd.DataFrame({
        "dias_desde_radicacion": [5, 45, 120],
        "longitud_descripcion": [90, 65, 75],
        "cantidad_adjuntos": [1, 3, 5],
        "tipo": ["Petición", "Queja", "Reclamo"],
    })[COLUMNAS_ENTRADA]

    # 3. Predecir prioridad alta (0 o 1) y su probabilidad
    predicciones = modelo.predict(nuevas_pqrs)
    probabilidades = modelo.predict_proba(nuevas_pqrs)[:, 1]

    # 4. Mostrar los resultados
    resultados = nuevas_pqrs.copy()
    resultados["probabilidad_prioridad_alta_%"] = (
        probabilidades * 100
    ).round(1)
    resultados["prioridad_predicha"] = [
        "Alta" if valor == 1 else "No alta"
        for valor in predicciones
    ]

    print("Predicciones de prioridad de PQRS (modelo cargado, sin reentrenar):")
    print(resultados.to_string(index=False))
    print("\nRecordatorio: datos sintéticos con etiqueta circular (fuga)")
    print("metodológica) y uso exclusivamente académico.")


if __name__ == "__main__":
    main()
