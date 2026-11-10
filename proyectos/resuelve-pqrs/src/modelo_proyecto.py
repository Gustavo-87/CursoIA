
from pathlib import Path

import joblib
import pandas as pd

from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
)

BASE_DIR = Path(__file__).resolve().parents[1]
DATASET = BASE_DIR / "data" / "pqrs_ml_segundo_corte.csv"

# 1. Cargar datos originales del Avance 2
df = pd.read_csv(DATASET)

columnas = ["dias_desde_radicacion", "longitud_descripcion"]
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

# 3. Definir tres modelos
modelos = {
    "Regresión logística": Pipeline([
        ("escalado", StandardScaler()),
        ("modelo", LogisticRegression(max_iter=1000))
    ]),
    "KNN": Pipeline([
        ("escalado", StandardScaler()),
        ("modelo", KNeighborsClassifier(n_neighbors=3))
    ]),
    "Árbol de decisión": Pipeline([
        ("escalado", StandardScaler()),
        ("modelo", DecisionTreeClassifier(
            max_depth=3, random_state=42
        ))
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
        cv=3,
        scoring="accuracy"
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

# 6. Guardar el modelo
ruta_modelo = BASE_DIR / "modelo_pqrs_final.joblib"
joblib.dump(mejor_modelo, ruta_modelo)

print(f"\nModelo guardado: {ruta_modelo}")
