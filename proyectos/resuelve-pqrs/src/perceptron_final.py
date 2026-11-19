
from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
)

BASE_DIR = Path(__file__).resolve().parents[1]

# 1. Cargar dataset final
df = pd.read_csv(BASE_DIR / "data" / "pqrs_final_150.csv")

# Usaremos las mismas dos entradas del perceptrón original
columnas = ["dias_desde_radicacion", "longitud_descripcion"]
X = df[columnas].to_numpy(dtype=float)
y = df["prioridad_alta"].to_numpy(dtype=int)

# 2. Separar entrenamiento y prueba
X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

# 3. Estandarizar sin utilizar información de prueba
escalador = StandardScaler()
X_train = escalador.fit_transform(X_train)
X_test = escalador.transform(X_test)

# 4. Función sigmoide
def sigmoide(z):
    z = np.clip(z, -500, 500)
    return 1 / (1 + np.exp(-z))


# 5. Entrenar perceptrón desde cero
rng = np.random.default_rng(42)
pesos = rng.normal(0, 0.01, X_train.shape[1])
sesgo = 0.0

tasa_aprendizaje = 0.1
epocas = 10000
perdidas = []

for epoca in range(epocas):
    z = X_train @ pesos + sesgo
    probabilidades = sigmoide(z)

    # Entropía cruzada binaria
    p = np.clip(probabilidades, 1e-10, 1 - 1e-10)
    perdida = -np.mean(
        y_train * np.log(p)
        + (1 - y_train) * np.log(1 - p)
    )
    perdidas.append(perdida)

    # Descenso del gradiente
    error = probabilidades - y_train
    gradiente_pesos = X_train.T @ error / len(y_train)
    gradiente_sesgo = np.mean(error)

    pesos -= tasa_aprendizaje * gradiente_pesos
    sesgo -= tasa_aprendizaje * gradiente_sesgo

# 6. Evaluar con datos no vistos
probabilidades_test = sigmoide(X_test @ pesos + sesgo)
predicciones = (probabilidades_test >= 0.5).astype(int)

print("PERCEPTRÓN FINAL - NUMPY")
print(f"Entrenamiento: {len(X_train)}")
print(f"Prueba: {len(X_test)}")
print(f"Pérdida inicial: {perdidas[0]:.4f}")
print(f"Pérdida final: {perdidas[-1]:.4f}")
print(f"Pesos: {pesos}")
print(f"Sesgo: {sesgo:.4f}")

print("\nMétricas de prueba:")
print(f"Exactitud: {accuracy_score(y_test, predicciones):.3f}")
print(f"Precisión: {precision_score(y_test, predicciones, zero_division=0):.3f}")
print(f"Recall: {recall_score(y_test, predicciones, zero_division=0):.3f}")
print(f"F1: {f1_score(y_test, predicciones, zero_division=0):.3f}")

print("\nMatriz de confusión:")
print(confusion_matrix(y_test, predicciones, labels=[0, 1]))

# 7. Guardar curva de aprendizaje
ruta_graficos = BASE_DIR / "graficos_final"
ruta_graficos.mkdir(exist_ok=True)

plt.figure(figsize=(8, 5))
plt.plot(perdidas)
plt.title("Curva de aprendizaje - Perceptrón NumPy")
plt.xlabel("Épocas")
plt.ylabel("Pérdida logarítmica")
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig(ruta_graficos / "curva_perceptron.png", dpi=150)
plt.close()

print("\nGráfico guardado: graficos_final/curva_perceptron.png")
