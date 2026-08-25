import pandas as pd

datos = pd.read_csv("data/pqrs/pqrs.csv")

print(datos)

print("\nPQRS en revisión:")

pqrs_en_revision = datos[datos["estado"] == "En revisión"]

print(pqrs_en_revision)

promedio_dias = datos["dias_abierta"].mean()

print("\nPromedio de días abiertos:")
print(promedio_dias)

pqrs_mas_antigua = datos.loc[datos["dias_abierta"].idxmax()]

print("\nPQRS con más días abierta:")
print(pqrs_mas_antigua)

conteo_tipos = datos["tipo"].value_counts()

print("\nCantidad de PQRS por tipo:")
print(conteo_tipos)
