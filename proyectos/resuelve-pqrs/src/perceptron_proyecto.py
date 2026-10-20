"""Requisito D: neurona sigmoide con pérdida logarítmica y gradiente NumPy."""

import csv
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


BASE_DIR = Path(__file__).resolve().parents[1]
TASA_APRENDIZAJE = 0.1
EPOCAS = 10000


def cargar_datos(ruta):
    """Lee, sin modificarlo, el CSV de las dos entradas y el objetivo."""
    with open(ruta, encoding="utf-8", newline="") as archivo:
        columnas = next(csv.reader(archivo), None)
        if columnas != ["dias_desde_radicacion", "longitud_descripcion", "prioridad_alta"]:
            raise ValueError("Se requieren las dos entradas y prioridad_alta, en ese orden.")
        datos = np.loadtxt(archivo, delimiter=",", ndmin=2)
    if (
        datos.shape != (12, 3)
        or not np.isfinite(datos).all()
        or (datos[:, :2] < 0).any()
        or set(datos[:, 2]) != {0, 1}
    ):
        raise ValueError("El CSV debe conservar los 12 casos válidos y las dos clases 0/1.")
    return datos[:, :2], datos[:, 2]


def estandarizar(X):
    """Estandarización poblacional: (X - media) / desviación, ddof=0."""
    X = np.asarray(X, dtype=float)
    if X.ndim != 2 or X.shape[0] == 0 or X.shape[1] != 2 or not np.isfinite(X).all():
        raise ValueError("Se requieren dos entradas numéricas finitas y al menos una fila.")
    media = X.mean(axis=0)
    desviacion = X.std(axis=0)
    if (desviacion == 0).any():
        raise ValueError("No es posible estandarizar una entrada constante.")
    return (X - media) / desviacion, media, desviacion


def sigmoide(z):
    """Sigmoide estable sin desbordamiento para logits de gran magnitud."""
    z = np.asarray(z, dtype=float)
    exponencial = np.exp(-np.abs(z))
    return np.where(z >= 0, 1 / (1 + exponencial), exponencial / (1 + exponencial))


def perdida_logaritmica(y, z):
    """Entropía cruzada binaria media calculada desde logits, sin log(0)."""
    return float(np.mean(np.logaddexp(0.0, z) - y * z))


def gradientes(X, y, w, b):
    error = sigmoide(X @ w + b) - y
    return X.T @ error / len(y), float(error.mean())


def entrenar(X, y, tasa_aprendizaje=TASA_APRENDIZAJE, epocas=EPOCAS):
    """Descenso del gradiente por lotes, sin aleatoriedad ni Scikit-Learn."""
    X, y = np.asarray(X, dtype=float), np.asarray(y, dtype=float)
    if (
        X.ndim != 2 or X.shape[1] != 2 or len(X) == 0 or y.shape != (len(X),)
        or not np.isfinite(X).all() or not np.isin(y, [0, 1]).all()
        or not np.isfinite(tasa_aprendizaje) or tasa_aprendizaje <= 0
        or not isinstance(epocas, int) or epocas <= 0
    ):
        raise ValueError("Entradas, objetivo o parámetros de entrenamiento inválidos.")
    w = np.zeros(2, dtype=float)
    b = 0.0
    perdidas = [perdida_logaritmica(y, X @ w + b)]
    for _ in range(epocas):
        dw, db = gradientes(X, y, w, b)
        w -= tasa_aprendizaje * dw
        b -= tasa_aprendizaje * db
        perdida = perdida_logaritmica(y, X @ w + b)
        if not np.isfinite(perdida):
            raise FloatingPointError("El entrenamiento produjo una pérdida no finita.")
        perdidas.append(perdida)
    return w, b, np.array(perdidas)


def generar_graficos(X, y, media, desviacion, w, b, perdidas, directorio):
    directorio.mkdir(parents=True, exist_ok=True)
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.plot(np.arange(len(perdidas)), perdidas)
    ax.set(title="Aprendizaje de la neurona sigmoide",
           xlabel="Época (0 = antes de entrenar)", ylabel="Pérdida logarítmica media")
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    fig.savefig(directorio / "curva_aprendizaje.png", dpi=150)
    plt.close(fig)

    # Se grafica en unidades originales; la malla usa la misma estandarización.
    margen = np.ptp(X, axis=0) * 0.1
    minimo, maximo = X.min(axis=0) - margen, X.max(axis=0) + margen
    xx, yy = np.meshgrid(np.linspace(minimo[0], maximo[0], 200),
                         np.linspace(minimo[1], maximo[1], 200))
    malla = np.column_stack((xx.ravel(), yy.ravel()))
    probabilidades = sigmoide(((malla - media) / desviacion) @ w + b).reshape(xx.shape)
    fig, ax = plt.subplots(figsize=(9, 6))
    ax.contourf(xx, yy, probabilidades, levels=[0, 0.5, 1],
                colors=["steelblue", "darkorange"], alpha=0.15)
    frontera = ax.contour(xx, yy, probabilidades, levels=[0.5], colors="black")
    ax.clabel(frontera, fmt={0.5: "p = 0.5"}, inline=True)
    for clase, color, marcador, etiqueta in [
        (0, "steelblue", "o", "0: media/baja"), (1, "darkorange", "X", "1: alta"),
    ]:
        puntos = X[y == clase]
        ax.scatter(puntos[:, 0], puntos[:, 1], c=color, marker=marcador, s=80,
                   label=etiqueta, edgecolors="black", linewidths=0.5)
    ax.set(title="Frontera de decisión: prioridad alta (p = 0.5)",
           xlabel="Días desde la radicación", ylabel="Longitud de la descripción (caracteres)")
    ax.legend(title="Etiqueta académica real")
    fig.tight_layout()
    fig.savefig(directorio / "frontera_decision.png", dpi=150)
    plt.close(fig)


def main():
    X, y = cargar_datos(BASE_DIR / "data" / "pqrs_ml_segundo_corte.csv")
    X_estandar, media, desviacion = estandarizar(X)
    w, b, perdidas = entrenar(X_estandar, y)
    predicciones = (sigmoide(X_estandar @ w + b) >= 0.5).astype(int)
    aciertos = int(np.sum(predicciones == y))
    print("NEURONA SIGMOIDE - REQUISITO D (NumPy, sin Scikit-Learn)")
    print(f"Casos: {len(y)}; épocas: {EPOCAS}; tasa: {TASA_APRENDIZAJE}; inicio: w=0, b=0")
    print("Estandarización (ddof=0) sobre los 12 casos de entrenamiento:")
    print(f"Medias: {media}; desviaciones: {desviacion}")
    print(f"Pesos sobre entradas estandarizadas: w1={w[0]:.10f}, w2={w[1]:.10f}, b={b:.10f}")
    print(f"Pérdida inicial: {perdidas[0]:.10f}")
    print(f"Pérdida final: {perdidas[-1]:.10f}")
    print(f"Exactitud de entrenamiento: {aciertos}/{len(y)} = {aciertos / len(y):.2%}")
    print("Predicciones (orden del CSV):", predicciones.tolist())
    for nombre, peso in zip(["días", "longitud"], w):
        efecto = "aumenta" if peso > 0 else "disminuye" if peso < 0 else "no cambia"
        print(f"Peso de {nombre}: {peso:+.6f}; {efecto} la probabilidad al aumentar esta entrada, "
              "manteniendo la otra fija (no implica causalidad).")
    print("La exactitud es de entrenamiento, sin evaluación independiente. "
          "12 casos sintéticos y etiquetas subjetivas no permiten generalizar.")
    directorio = BASE_DIR / "informes" / "segundo_corte" / "perceptron"
    generar_graficos(X, y, media, desviacion, w, b, perdidas, directorio)
    print(f"Gráficos guardados en: {directorio}")


if __name__ == "__main__":
    main()
