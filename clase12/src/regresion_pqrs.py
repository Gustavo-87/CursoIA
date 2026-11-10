
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

# 1. Generar datos sintéticos reproducibles
rng = np.random.default_rng(42)
n = 150

df = pd.DataFrame({
    "cantidad_adjuntos": rng.integers(0, 7, n),
    "complejidad": rng.integers(1, 6, n),
    "cantidad_interacciones": rng.integers(1, 11, n)
})

# Variable objetivo: días de resolución simulados
df["dias_resolucion"] = (
    2
    + 1.5 * df["cantidad_adjuntos"]
    + 4 * df["complejidad"]
    + 0.8 * df["cantidad_interacciones"]
    + rng.normal(0, 3, n)
).clip(lower=1).round(1)

df.to_csv("clase12/data/rendimiento_pqrs.csv", index=False)

# 2. Definir entradas y variable objetivo
entradas = [
    "cantidad_adjuntos",
    "complejidad",
    "cantidad_interacciones"
]

X = df[entradas]
y = df["dias_resolucion"]

# 3. Separar entrenamiento y prueba
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# 4. Entrenar modelo
modelo = Pipeline([
    ("escalado", StandardScaler()),
    ("modelo", LinearRegression())
])

modelo.fit(X_train, y_train)
predicciones = modelo.predict(X_test)

# 5. Evaluar el modelo
mae = mean_absolute_error(y_test, predicciones)
rmse = np.sqrt(mean_squared_error(y_test, predicciones))
r2 = r2_score(y_test, predicciones)

print("Resultados de regresión lineal:")
print(f"Entrenamiento: {len(X_train)}")
print(f"Prueba: {len(X_test)}")
print(f"MAE: {mae:.2f} días")
print(f"RMSE: {rmse:.2f} días")
print(f"R²: {r2:.3f}")

# 6. Comparación gráfica
plt.figure(figsize=(7, 6))
plt.scatter(y_test, predicciones, alpha=0.7)

limites = [
    min(y_test.min(), predicciones.min()),
    max(y_test.max(), predicciones.max())
]

plt.plot(limites, limites, "r--", label="Predicción perfecta")
plt.xlabel("Días reales simulados")
plt.ylabel("Días predichos")
plt.title("Regresión lineal - PQRS")
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()

plt.savefig("clase12/real_vs_predicho.png", dpi=150)
plt.close()

print("Gráfico guardado: clase12/real_vs_predicho.png")
