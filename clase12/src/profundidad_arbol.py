
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier

# 1. Cargar datos sintéticos de PQRS
df = pd.read_csv("clase12/data/pqrs_simuladas.csv")

X = df[["dias_abierta", "cantidad_adjuntos"]]
y = (df["estado"] == "Cerrada").astype(int)

# 2. Separar entrenamiento y prueba
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# 3. Entrenar árboles con diferentes profundidades
resultados = []

for profundidad in range(1, 13):
    arbol = DecisionTreeClassifier(
        max_depth=profundidad,
        random_state=42
    )

    arbol.fit(X_train, y_train)

    resultados.append({
        "Profundidad": profundidad,
        "Entrenamiento": arbol.score(X_train, y_train),
        "Prueba": arbol.score(X_test, y_test)
    })

# 4. Mostrar comparación
tabla = pd.DataFrame(resultados)
print(tabla.round(3).to_string(index=False))

# 5. Generar gráfico
plt.figure(figsize=(8, 5))

plt.plot(
    tabla["Profundidad"],
    tabla["Entrenamiento"],
    marker="o",
    label="Entrenamiento"
)

plt.plot(
    tabla["Profundidad"],
    tabla["Prueba"],
    marker="s",
    label="Prueba"
)

plt.title("Sobreajuste: profundidad del árbol - PQRS")
plt.xlabel("Profundidad del árbol")
plt.ylabel("Exactitud")
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()

plt.savefig("clase12/sobreajuste_arbol.png", dpi=150)
plt.close()

print("\nGráfico guardado: clase12/sobreajuste_arbol.png")
