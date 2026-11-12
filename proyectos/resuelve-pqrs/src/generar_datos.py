
from pathlib import Path

import numpy as np
import pandas as pd

BASE_DIR = Path(__file__).resolve().parents[1]
RUTA_SALIDA = BASE_DIR / "data" / "pqrs_final_150.csv"

# Semilla para obtener siempre los mismos resultados
rng = np.random.default_rng(42)
n = 150

# Datos sintéticos
df = pd.DataFrame({
    "dias_desde_radicacion": rng.integers(1, 151, n),
    "longitud_descripcion": rng.integers(30, 301, n),
    "tipo": rng.choice(
        ["Petición", "Queja", "Reclamo", "Solicitud", "Sugerencia"],
        size=n
    ),
    "cantidad_adjuntos": rng.integers(0, 6, n)
})

# Regla académica para simular la prioridad
puntaje = (
    0.025 * df["dias_desde_radicacion"]
    + 0.008 * df["longitud_descripcion"]
    + 0.25 * df["cantidad_adjuntos"]
    + df["tipo"].map({
        "Petición": 0.2,
        "Queja": 0.8,
        "Reclamo": 1.0,
        "Solicitud": 0.3,
        "Sugerencia": 0.1
    })
    + rng.normal(0, 1.2, n)
)

# Clasificación binaria
df["prioridad_alta"] = (puntaje >= np.quantile(puntaje, 0.80)).astype(int)

# Guardar dataset
RUTA_SALIDA.parent.mkdir(parents=True, exist_ok=True)
df.to_csv(RUTA_SALIDA, index=False)

print(f"Dataset generado: {RUTA_SALIDA}")
print(f"Total de registros: {len(df)}")
print("\nDistribución de prioridad:")
print(df["prioridad_alta"].value_counts())
print("\nValores faltantes:")
print(df.isna().sum())
