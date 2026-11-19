"""Modelo final de PQRS con Scikit-Learn (Clase 12).

Contrato único de variables de entrada (entrenamiento y predicción):
    - dias_desde_radicacion (numérica)
    - longitud_descripcion  (numérica)
    - cantidad_adjuntos     (numérica)
    - tipo                  (categórica)
Variable objetivo: prioridad_alta (0 = no alta, 1 = alta).

LIMITACIONES METODOLÓGICAS (visibles, no ocultar):
- Los datos de data/pqrs_final_150.csv son SINTÉTICOS, generados por código
  (src/generar_datos.py, semilla 42). No provienen de PQRS reales.
- CIRCULARIDAD / FUGA METODOLÓGICA: la variable objetivo prioridad_alta fue
  creada a partir de las MISMAS variables de entrada (una regla ponderada de
  días, longitud, adjuntos y tipo, más ruido). El modelo solo puede aprender
  esa regla generadora; sus métricas NO demuestran validez predictiva real.
- Sistema ACADÉMICO, no apto para asignar prioridades en operación real.
"""

from pathlib import Path

import joblib
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
    ConfusionMatrixDisplay,
)

BASE_DIR = Path(__file__).resolve().parents[1]
DATASET = BASE_DIR / "data" / "pqrs_final_150.csv"
RUTA_MODELO = BASE_DIR / "modelo_pqrs_final.joblib"
RUTA_GRAFICOS = BASE_DIR / "graficos_final"

# Contrato único de variables (idéntico al de src/usar_modelo.py)
COLUMNAS_NUMERICAS = [
    "dias_desde_radicacion",
    "longitud_descripcion",
    "cantidad_adjuntos",
]
COLUMNA_CATEGORICA = "tipo"
COLUMNAS_ENTRADA = COLUMNAS_NUMERICAS + [COLUMNA_CATEGORICA]
OBJETIVO = "prioridad_alta"


def crear_preprocesador():
    """Numéricas: estandarización. Categórica: one-hot tolerante a desconocidos."""
    return ColumnTransformer([
        ("numericas", StandardScaler(), COLUMNAS_NUMERICAS),
        ("categorica", OneHotEncoder(handle_unknown="ignore"), [COLUMNA_CATEGORICA]),
    ])


def crear_modelos():
    """Tres clasificadores comparados, cada uno dentro de un Pipeline."""
    return {
        "Regresión logística": Pipeline([
            ("preparacion", crear_preprocesador()),
            ("modelo", LogisticRegression(max_iter=1000)),
        ]),
        "KNN": Pipeline([
            ("preparacion", crear_preprocesador()),
            ("modelo", KNeighborsClassifier(n_neighbors=3)),
        ]),
        "Árbol de decisión": Pipeline([
            ("preparacion", crear_preprocesador()),
            ("modelo", DecisionTreeClassifier(max_depth=3, random_state=42)),
        ]),
    }


def graficar_evaluacion(y_test, pred, probabilidades, nombre_mejor):
    """Matriz de confusión y real vs predicho, regenerables desde este código."""
    RUTA_GRAFICOS.mkdir(exist_ok=True)

    # 1. Matriz de confusión
    matriz = confusion_matrix(y_test, pred, labels=[0, 1])
    fig, ax = plt.subplots(figsize=(6, 5))
    ConfusionMatrixDisplay(
        confusion_matrix=matriz,
        display_labels=["No alta", "Alta"],
    ).plot(ax=ax, cmap="Blues", values_format="d", colorbar=False)
    ax.set_title(f"Matriz de confusión - {nombre_mejor} (prueba)")
    fig.tight_layout()
    fig.savefig(RUTA_GRAFICOS / "matriz_confusion.png", dpi=150)
    plt.close(fig)

    # 2. Real vs predicho: probabilidad predicha según la clase real
    y_test = np.asarray(y_test)
    pred = np.asarray(pred)
    acierto = np.where(pred == y_test, "Correcto", "Incorrecto")
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.stripplot(
        x=y_test, y=probabilidades, hue=acierto,
        hue_order=["Correcto", "Incorrecto"],
        palette={"Correcto": "steelblue", "Incorrecto": "crimson"},
        jitter=0.15, size=9, alpha=0.85, ax=ax,
    )
    ax.axhline(0.5, color="black", linestyle="--", linewidth=1,
               label="Umbral p = 0.5")
    ax.set(
        title=f"Real vs predicho - {nombre_mejor} (casos de prueba)",
        xlabel="Clase real (0 = no alta, 1 = alta)",
        ylabel="Probabilidad predicha de prioridad alta",
    )
    ax.set_xticks([0, 1])
    ax.set_xticklabels(["0: no alta", "1: alta"])
    ax.set_ylim(-0.05, 1.05)
    ax.grid(True, axis="y", alpha=0.3)
    fig.tight_layout()
    fig.savefig(RUTA_GRAFICOS / "real_vs_predicho.png", dpi=150)
    plt.close(fig)

    print(f"Gráficos guardados en: {RUTA_GRAFICOS}")


def main():
    # 1. Cargar datos (sintéticos; ver docstring por la fuga metodológica)
    df = pd.read_csv(DATASET)
    print("AVISO: datos SINTÉTICOS; prioridad_alta se generó a partir de las")
    print("mismas variables de entrada (circularidad / fuga metodológica).")
    print("Uso académico; no apto para operación real.\n")

    X = df[COLUMNAS_ENTRADA]
    y = df[OBJETIVO]

    # 2. Separar entrenamiento y prueba (estratificado, reproducible)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y,
        test_size=0.2,
        random_state=42,
        stratify=y,
    )
    print(f"Entrenamiento: {len(X_train)} | Prueba: {len(X_test)}")
    print(f"Variables de entrada: {COLUMNAS_ENTRADA}\n")

    # 3. Definir los tres modelos (Pipeline: preprocesamiento + clasificador)
    modelos = crear_modelos()

    # 4. Entrenar y evaluar cada modelo
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
            scoring="f1",
        )

        resultados.append({
            "Modelo": nombre,
            "Exactitud": accuracy_score(y_test, pred),
            "Precisión": precision_score(y_test, pred, zero_division=0),
            "Recall": recall_score(y_test, pred, zero_division=0),
            "F1": f1_score(y_test, pred, zero_division=0),
            "Val. cruzada (F1)": cv.mean(),
        })

    tabla = pd.DataFrame(resultados)
    print("Comparación de modelos (conjunto de prueba):")
    print(tabla.round(3).to_string(index=False))

    # 5. Seleccionar el mejor modelo según F1 de validación cruzada
    nombre_mejor = tabla.loc[
        tabla["Val. cruzada (F1)"].idxmax(), "Modelo"
    ]
    mejor_modelo = modelos[nombre_mejor]

    pred_mejor = mejor_modelo.predict(X_test)
    probabilidades_mejor = mejor_modelo.predict_proba(X_test)[:, 1]
    matriz = confusion_matrix(y_test, pred_mejor, labels=[0, 1])

    print(f"\nMejor modelo: {nombre_mejor} "
          f"(mayor F1 promedio de validación cruzada)")
    print("Métricas del mejor modelo (conjunto de prueba):")
    print(f"  Exactitud : {accuracy_score(y_test, pred_mejor):.3f}")
    print(f"  Precisión : {precision_score(y_test, pred_mejor, zero_division=0):.3f}")
    print(f"  Recall    : {recall_score(y_test, pred_mejor, zero_division=0):.3f}")
    print(f"  F1        : {f1_score(y_test, pred_mejor, zero_division=0):.3f}")
    print(f"  F1 validación cruzada (5 pliegues): "
          f"{tabla.loc[tabla['Modelo'] == nombre_mejor, 'Val. cruzada (F1)'].iloc[0]:.3f}")
    print("\nMatriz de confusión (filas = real, columnas = predicho; [0, 1]):")
    print(matriz)

    # 6. Gráficos de evaluación regenerables desde este código
    graficar_evaluacion(y_test, pred_mejor, probabilidades_mejor, nombre_mejor)

    # 7. Guardar el mejor modelo con joblib
    joblib.dump(mejor_modelo, RUTA_MODELO)
    print(f"\nModelo guardado: {RUTA_MODELO}")
    print("Recordatorio: datos sintéticos con etiqueta circular (fuga)")
    print("y uso exclusivamente académico.")


if __name__ == "__main__":
    main()
