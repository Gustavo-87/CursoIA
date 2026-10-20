"""
Implementación de las compuertas lógicas OR y NOT.
"""

import matplotlib.pyplot as plt


def escalon(z):
    return 1 if z >= 0 else 0


def neurona(x1, x2, w1, w2, b):
    z = w1 * x1 + w2 * x2 + b
    return escalon(z)

# ============================================================
# 1. Compuerta OR: datos y parámetros
# ============================================================
datos_or = [
    (0, 0, 0),
    (0, 1, 1),
    (1, 0, 1),
    (1, 1, 1),
]

w1_or = 0.1
w2_or = 0.1
b_or = 0.0
tasa_aprendizaje = 0.1
errores_or = []
print("=" * 60)
print("ENTRENAMIENTO DE LA COMPUERTA OR")
print("=" * 60)

for epoca in range(10):
    error_total = 0
    print(f"--- Época {epoca + 1} ---")

    for x1, x2, y_real in datos_or:
        y_pred = neurona(x1, x2, w1_or, w2_or, b_or)

        error = y_real - y_pred
        error_total += abs(error)

        w1_or += tasa_aprendizaje * error * x1
        w2_or += tasa_aprendizaje * error * x2
        b_or += tasa_aprendizaje * error

    errores_or.append(error_total)
    print(f"Error total: {error_total}")

    if error_total == 0:
        print(f"La compuerta OR aprendió en {epoca + 1} épocas.\n")
        break
print("PRUEBA FINAL OR")

for x1, x2, y_real in datos_or:
    y_pred = neurona(x1, x2, w1_or, w2_or, b_or)
    estado = "OK" if y_pred == y_real else "X"

    print(
        f"{estado} Entrada: ({x1}, {x2}) | "
        f"Esperado: {y_real} | Predicho: {y_pred}"
    )
    plt.figure(figsize=(8, 5))
plt.plot(
    range(1, len(errores_or) + 1),
    errores_or,
    marker="o",
    color="blue"
)
plt.title("Evolución del Error - Compuerta OR")
plt.xlabel("Época")
plt.ylabel("Error Total")
plt.grid(True)
plt.savefig("evolucion_error_or.png", dpi=150)
plt.close()

print("Gráfico guardado: evolucion_error_or.png")
# ============================================================
# 2. Compuerta NOT: neurona, datos y parámetros
# ============================================================
def neurona_not(x1, w1, b):
    z = w1 * x1 + b
    return escalon(z)


datos_not = [
    (0, 1),
    (1, 0),
]

w1_not = 0.1
b_not = 0.0
errores_not = []
print("=" * 60)
print("ENTRENAMIENTO DE LA COMPUERTA NOT")
print("=" * 60)

for epoca in range(10):
    error_total = 0
    print(f"--- Época {epoca + 1} ---")

    for x1, y_real in datos_not:
        y_pred = neurona_not(x1, w1_not, b_not)

        error = y_real - y_pred
        error_total += abs(error)

        w1_not += tasa_aprendizaje * error * x1
        b_not += tasa_aprendizaje * error

    errores_not.append(error_total)
    print(f"Error total: {error_total}")

    if error_total == 0:
        print(f"La compuerta NOT aprendió en {epoca + 1} épocas.\n")
        break
print("PRUEBA FINAL NOT")

for x1, y_real in datos_not:
    y_pred = neurona_not(x1, w1_not, b_not)
    estado = "OK" if y_pred == y_real else "X"

    print(
        f"{estado} Entrada: ({x1}) | "
        f"Esperado: {y_real} | Predicho: {y_pred}"
    )
    plt.figure(figsize=(8, 5))
plt.plot(
    range(1, len(errores_not) + 1),
    errores_not,
    marker="o",
    color="green"
)
plt.title("Evolución del Error - Compuerta NOT")
plt.xlabel("Época")
plt.ylabel("Error Total")
plt.grid(True)
plt.savefig("evolucion_error_not.png", dpi=150)
plt.close()

print("Gráfico guardado: evolucion_error_not.png")
