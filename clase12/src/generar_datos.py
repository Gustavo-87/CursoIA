
from pathlib import Path
import numpy as np
import pandas as pd

rng = np.random.default_rng(42)
n = 120

tipos = ["Petición", "Queja", "Reclamo", "Sugerencia"]

df = pd.DataFrame({
    "radicado": [f"PQRS-{i:03d}" for i in range(1, n + 1)],
    "tipo": rng.choice(tipos, size=n),
    "dias_abierta": rng.integers(1, 61, size=n),
    "cantidad_adjuntos": rng.integers(0, 6, size=n),
})

# Estados simulados con relaciones estadísticas y variación aleatoria
puntaje = (
    0.09 * df["dias_abierta"]
    + 0.25 * df["cantidad_adjuntos"]
    + rng.normal(0, 1.8, n)
)

df["estado"] = np.select(
    [puntaje < 2.5, puntaje < 5.0],
    ["Radicada", "En revisión"],
    default="Cerrada"
)

ruta = Path("clase12/data/pqrs_simuladas.csv")
ruta.parent.mkdir(parents=True, exist_ok=True)
df.to_csv(ruta, index=False)

print(f"Dataset generado: {ruta}")
print(f"Registros: {len(df)}")
print(df["estado"].value_counts())
