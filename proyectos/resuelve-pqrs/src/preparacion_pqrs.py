import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

sns.set_theme(style="whitegrid", context="talk")

def cargar_datos(archivo_csv):
    """Carga el archivo CSV de PQRS como un DataFrame."""
    try:
        df = pd.read_csv(archivo_csv)
        print(
            f"Datos cargados: {df.shape[0]} filas y "
            f"{df.shape[1]} columnas."
        )
        return df
    except FileNotFoundError:
        print(f"No se encontró el archivo: {archivo_csv}")
        return None
    
def explorar_datos(df):
    """Muestra información básica del conjunto de PQRS."""
    print("\nPRIMERAS 5 FILAS:")
    print(df.head())

    print("\nINFORMACIÓN GENERAL:")
    df.info()

    print("\nESTADÍSTICAS DESCRIPTIVAS:")
    print(df.describe(include="all"))

    print("\nVALORES NULOS POR COLUMNA:")
    print(df.isnull().sum())  
def limpiar_datos(df):
    """Convierte datos numéricos y maneja valores nulos."""
    df_limpio = df.copy()

    df_limpio["dias_desde_radicacion"] = pd.to_numeric(
        df_limpio["dias_desde_radicacion"],
        errors="coerce"
    )

    if df_limpio["dias_desde_radicacion"].isnull().any():
        mediana_dias = df_limpio["dias_desde_radicacion"].median()
        df_limpio["dias_desde_radicacion"] = (
            df_limpio["dias_desde_radicacion"].fillna(mediana_dias)
        )
        print(
            "Valores nulos en días reemplazados por la mediana: "
            f"{mediana_dias}"
        )
    else:
        print("\nNo se encontraron valores nulos en días.")
    df_limpio["longitud_descripcion"] = (
        df_limpio["descripcion"].fillna("").str.len()
    )
    print("Columna 'longitud_descripcion' creada.")
    return df_limpio

def visualizar_datos(df):
    """Genera visualizaciones con Seaborn."""
    plt.figure(figsize=(8, 5))
    sns.histplot(
        data=df,
        x="dias_desde_radicacion",
        bins=6,
        kde=True,
        color="steelblue"
    )
    plt.title("Distribución de días desde la radicación")
    plt.xlabel("Días desde la radicación")
    plt.ylabel("Cantidad de PQRS")
    plt.tight_layout()
    plt.savefig("histograma_dias_pqrs.png", dpi=150)
    plt.close()

    plt.figure(figsize=(8, 5))
    orden_tipos = df["tipo"].value_counts().index
    sns.countplot(
        data=df,
        x="tipo",
        order=orden_tipos,
        color="seagreen"
    )
    plt.title("Cantidad de PQRS por tipo")
    plt.xlabel("Tipo de PQRS")
    plt.ylabel("Cantidad")
    plt.tight_layout()
    plt.savefig("pqrs_por_tipo.png", dpi=150)
    plt.close()

    print("Gráfico guardado: pqrs_por_tipo.png")

    print("Gráfico guardado: histograma_dias_pqrs.png")

    plt.figure(figsize=(8, 5))
    sns.scatterplot(
        data=df,
        x="dias_desde_radicacion",
        y="longitud_descripcion",
        hue="tipo",
        s=100
    )
    plt.title("Antigüedad y longitud de la descripción")
    plt.xlabel("Días desde la radicación")
    plt.ylabel("Caracteres de la descripción")
    plt.tight_layout()
    plt.savefig("antiguedad_vs_descripcion.png", dpi=150)
    plt.close()

    print("Gráfico guardado: antiguedad_vs_descripcion.png")

def preparar_ml(df):
    # Codifica variables categóricas para un futuro modelo.
    df_ml = df.copy()

    df_ml = pd.get_dummies(
        df_ml,
        columns=["tipo", "estado"],
        prefix=["tipo", "estado"],
        dtype=int
    )
    print("\nCodificación One-Hot aplicada a tipo y estado.")

    columnas_a_eliminar = ["radicado", "asunto", "descripcion"]
    df_ml = df_ml.drop(columns=columnas_a_eliminar, errors="ignore")
    print("Columnas de identificación y texto eliminadas de la copia para ML.")

    print("\nDATAFRAME PREPARADO PARA ML:")
    print(df_ml.head())

    return df_ml

def main():
    print("=" * 60)
    print("PREPARACIÓN DE DATOS DE PQRS")
    print("=" * 60)

    df = cargar_datos("data/pqrs.csv")

    if df is None:
        return

    explorar_datos(df)

    df_limpio = limpiar_datos(df)

    visualizar_datos(df_limpio)

    df_ml = preparar_ml(df_limpio)
    df_ml.to_csv("data/pqrs_preparadas_ml.csv", index=False)

    print("\nArchivo creado: data/pqrs_preparadas_ml.csv")
    print("Proceso completado.")


if __name__ == "__main__":
    main()



