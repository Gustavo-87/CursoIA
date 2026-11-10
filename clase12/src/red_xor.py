
import numpy as np
import pandas as pd

from sklearn.linear_model import LogisticRegression
from sklearn.neural_network import MLPClassifier

# 1. Datos de la compuerta XOR
X = np.array([
    [0, 0],
    [0, 1],
    [1, 0],
    [1, 1]
])

y = np.array([0, 1, 1, 0])

# 2. Entrenar una sola neurona
neurona = LogisticRegression()
neurona.fit(X, y)

# 3. Entrenar una red con 4 neuronas ocultas
red = MLPClassifier(
    hidden_layer_sizes=(4,),
    activation="tanh",
    solver="lbfgs",
    max_iter=1000,
    random_state=1
)

red.fit(X, y)

# 4. Comparar las predicciones
tabla = pd.DataFrame({
    "x1": X[:, 0],
    "x2": X[:, 1],
    "Esperado": y,
    "Una neurona": neurona.predict(X),
    "Red neuronal": red.predict(X)
})

print(tabla.to_string(index=False))

print(f"\nExactitud de una neurona: {neurona.score(X, y):.0%}")
print(f"Exactitud de la red neuronal: {red.score(X, y):.0%}")
