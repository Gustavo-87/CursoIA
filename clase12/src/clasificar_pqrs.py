
import joblib
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
)

# 1. Cargar datos simulados
df = pd.read_csv("clase12/data/pqrs_simuladas.csv")

# 2. Clasificación binaria: cerrada = 1, no cerrada = 0
X = df[["dias_abierta", "cantidad_adjuntos"]]
y = (df["estado"] == "Cerrada").astype(int)

# 3. Separar 80 % entrenamiento y 20 % prueba
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

print(f"Entrenamiento: {len(X_train)} | Prueba: {len(X_test)}")

# 4. Modelos
modelos = {
    "Regresión logística": Pipeline([
        ("escalado", StandardScaler()),
        ("modelo", LogisticRegression(max_iter=1000))
    ]),
    "KNN": Pipeline([
        ("escalado", StandardScaler()),
        ("modelo", KNeighborsClassifier(n_neighbors=5))
    ]),
    "Árbol de decisión": Pipeline([
        ("escalado", StandardScaler()),
        ("modelo", DecisionTreeClassifier(max_depth=3, random_state=42))
    ])
}

# 5. Entrenar y comparar
resultados = []

for nombre, modelo in modelos.items():
    modelo.fit(X_train, y_train)
    pred = modelo.predict(X_test)

    resultados.append({
        "Modelo": nombre,
        "Exactitud": accuracy_score(y_test, pred),
        "Precisión": precision_score(y_test, pred, zero_division=0),
        "Recall": recall_score(y_test, pred, zero_division=0),
        "F1": f1_score(y_test, pred, zero_division=0),
        "Val. cruzada": cross_val_score(
            modelo, X_train, y_train, cv=5, scoring="f1"
        ).mean()
    })

tabla = pd.DataFrame(resultados)
print("\nComparación de modelos:")
print(tabla.round(3).to_string(index=False))

# 6. Seleccionar el mejor modelo por F1
nombre_mejor = tabla.loc[tabla["F1"].idxmax(), "Modelo"]
mejor_modelo = modelos[nombre_mejor]

print(f"\nMejor modelo: {nombre_mejor}")

# 7. Matriz de confusión
matriz = confusion_matrix(
    y_test, mejor_modelo.predict(X_test), labels=[0, 1]
)

print("\nMatriz de confusión:")
print(matriz)

plt.figure(figsize=(6, 5))
sns.heatmap(
    matriz, annot=True, fmt="d", cmap="Blues",
    xticklabels=["No cerrada", "Cerrada"],
    yticklabels=["No cerrada", "Cerrada"]
)
plt.xlabel("Predicción")
plt.ylabel("Valor real")
plt.tight_layout()
plt.savefig("clase12/matriz_confusion.png")
plt.close()

# 8. Guardar modelo entrenado
joblib.dump(mejor_modelo, "clase12/modelo_pqrs.joblib")
print("\nModelo guardado: clase12/modelo_pqrs.joblib")
