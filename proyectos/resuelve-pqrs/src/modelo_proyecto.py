
from pathlib import Path

import joblib
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.metrics import ConfusionMatrixDisplay

from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
)

BASE_DIR = Path(__file__).resolve().parents[1]
DATASET = BASE_DIR / "data" / "pqrs_final_150.csv"

# 1. Cargar datos originales del Avance 2
df = pd.read_csv(DATASET)

columnas = ["dias_desde_radicacion", "longitud_descripcion", "cantidad_adjuntos", "tipo"]
X = df[columnas]
y = df["prioridad_alta"]

# 2. Separar entrenamiento y prueba
X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

print(f"Entrenamiento: {len(X_train)} | Prueba: {len(X_test)}")

# 3. Preparación y modelos
def crear_preprocesador():
    return ColumnTransformer([
        ("numericas", StandardScaler(), [
            "dias_desde_radicacion",
            "longitud_descripcion",
            "cantidad_adjuntos"
        ]),
        ("categorica", OneHotEncoder(handle_unknown="ignore"), ["tipo"])
    ])

modelos = {
    "Regresión logística": Pipeline([
        ("preparacion", crear_preprocesador()),
        ("modelo", LogisticRegression(max_iter=1000))
    ]),
    "KNN": Pipeline([
        ("preparacion", crear_preprocesador()),
        ("modelo", KNeighborsClassifier(n_neighbors=3))
    ]),
    "Árbol de decisión": Pipeline([
        ("preparacion", crear_preprocesador()),
        ("modelo", DecisionTreeClassifier(max_depth=3, random_state=42))
    ])
}

# 4. Entrenar y evaluar
resultados = []

for nombre, modelo in modelos.items():
    modelo.fit(X_train, y_train)
    pred = modelo.predict(X_test)

    # Validación cruzada con los datos de entrenamiento
    cv = cross_val_score(
        modelo,
        X_train,
        y_train,
        cv=5,
        scoring="f1"
    )

    resultados.append({
        "Modelo": nombre,
        "Exactitud": accuracy_score(y_test, pred),
        "Precisión": precision_score(y_test, pred, zero_division=0),
        "Recall": recall_score(y_test, pred, zero_division=0),
        "F1": f1_score(y_test, pred, zero_division=0),
        "Val. cruzada": cv.mean()
    })

tabla = pd.DataFrame(resultados)

print("\nComparación de modelos:")
print(tabla.round(3).to_string(index=False))

# 5. Seleccionar el mejor según validación cruzada
nombre_mejor = tabla.loc[
    tabla["Val. cruzada"].idxmax(), "Modelo"
]

mejor_modelo = modelos[nombre_mejor]

print(f"\nMejor modelo: {nombre_mejor}")
print("\nMatriz de confusión:")
print(confusion_matrix(
    y_test, mejor_modelo.predict(X_test), labels=[0, 1]
))

# Generar matriz de confusión
matriz = confusion_matrix(
    y_test, mejor_modelo.predict(X_test), labels=[0, 1]
)

fig, ax = plt.subplots(figsize=(6, 5))
ConfusionMatrixDisplay(
    confusion_matrix=matriz,
    display_labels=["No alta", "Alta"]
).plot(ax=ax, cmap="Blues", values_format="d", colorbar=False)

ax.set_title(f"Matriz de confusión - {nombre_mejor}")
fig.tight_layout()

ruta_graficos = BASE_DIR / "graficos_final"
ruta_graficos.mkdir(exist_ok=True)

fig.savefig(ruta_graficos / "matriz_confusion.png", dpi=150)
plt.close(fig)

print("Gráfico guardado: graficos_final/matriz_confusion.png")

# 6. Guardar el modelo
ruta_modelo = BASE_DIR / "modelo_pqrs_final.joblib"
joblib.dump(mejor_modelo, ruta_modelo)

print(f"\nModelo guardado: {ruta_modelo}")
