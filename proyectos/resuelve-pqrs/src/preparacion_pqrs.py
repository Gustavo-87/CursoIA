import argparse
from pathlib import Path

import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

sns.set_theme(style="whitegrid", context="talk")

BASE_DIR = Path(__file__).resolve().parents[1]

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

def visualizar_datos(df, segundo_corte=False):
    """Genera visualizaciones con Seaborn."""
    directorio = BASE_DIR / "informes" / "segundo_corte" if segundo_corte else BASE_DIR
    directorio.mkdir(parents=True, exist_ok=True)
    plt.figure(figsize=(8, 5))
    sns.histplot(
        data=df,
        x="dias_desde_radicacion",
        bins=6,
        kde=not segundo_corte,
        color="steelblue"
    )
    plt.title("Distribución de días desde la radicación")
    plt.xlabel("Días desde la radicación")
    plt.ylabel("Cantidad de PQRS")
    plt.tight_layout()
    plt.savefig(directorio / "histograma_dias_pqrs.png", dpi=150)
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
    plt.savefig(directorio / "pqrs_por_tipo.png", dpi=150)
    plt.close()

    print(f"Gráfico guardado: {directorio / 'pqrs_por_tipo.png'}")

    print(f"Gráfico guardado: {directorio / 'histograma_dias_pqrs.png'}")

    plt.figure(figsize=(8, 5))
    opciones = {"hue": "tipo"}
    if segundo_corte:
        opciones = {
            "hue": "prioridad_alta", "hue_order": [0, 1],
            "palette": {0: "steelblue", 1: "darkorange"},
            "style": "prioridad_alta", "style_order": [0, 1],
        }
    ax = sns.scatterplot(
        data=df,
        x="dias_desde_radicacion",
        y="longitud_descripcion",
        s=100,
        **opciones,
    )
    if segundo_corte:
        handles, _ = ax.get_legend_handles_labels()
        ax.legend(handles, ["0: media/baja", "1: alta"], title="prioridad_alta")
    plt.title("Entradas numéricas según prioridad" if segundo_corte
              else "Antigüedad y longitud de la descripción")
    plt.xlabel("Días desde la radicación")
    plt.ylabel("Caracteres de la descripción")
    plt.tight_layout()
    plt.savefig(directorio / "antiguedad_vs_descripcion.png", dpi=150)
    plt.close()

    print(f"Gráfico guardado: {directorio / 'antiguedad_vs_descripcion.png'}")

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

def validar_datos(df):
    """Audita los datos sin imputar ni descartar casos académicos."""
    columnas = {
        "radicado", "tipo", "estado", "dias_desde_radicacion", "asunto",
        "descripcion",
    }
    if set(df.columns) != columnas:
        raise ValueError("El CSV debe contener las seis columnas originales de PQRS.")

    dias = pd.to_numeric(df["dias_desde_radicacion"], errors="coerce")
    tipos_incorrectos = ~df["dias_desde_radicacion"].map(
        lambda valor: pd.api.types.is_number(valor) and not isinstance(valor, bool)
    )
    dias_invalidos = (
        dias.isna() | ~np.isfinite(dias) | (dias < 0) | (dias % 1 != 0)
        | df["dias_desde_radicacion"].map(lambda valor: isinstance(valor, bool))
    )
    texto_invalido = pd.Series(False, index=df.index)
    for columna in columnas - {"dias_desde_radicacion"}:
        texto_invalido |= ~df[columna].map(
            lambda valor: isinstance(valor, str) and bool(valor.strip())
        )

    categorias_invalidas = (
        ~df["tipo"].isin(["Petición", "Queja", "Reclamo", "Solicitud", "Sugerencia"])
        | ~df["estado"].isin(["Radicada", "En revisión", "Respondida", "Cerrada"])
    )
    auditoria = pd.Series({
        "nulos": int(df.isna().sum().sum()),
        "filas_duplicadas": int(df.duplicated().sum()),
        "radicados_duplicados": int(df["radicado"].duplicated().sum()),
        "tipos_dias_incorrectos": int(tipos_incorrectos.sum()),
        "dias_invalidos": int(dias_invalidos.sum()),
        "textos_invalidos": int(texto_invalido.sum()),
        "categorias_invalidas": int(categorias_invalidas.sum()),
    })
    print("\nAUDITORÍA DE CALIDAD:")
    print(auditoria.to_string())
    if auditoria.drop("tipos_dias_incorrectos").any():
        raise ValueError(
            "Hay datos inconsistentes; revisar la auditoría antes de corregirlos. "
            "No se imputaron valores ni se eliminaron registros."
        )
    return auditoria


def preparar_segundo_corte(df, etiquetas):
    """Combina anotaciones por radicado, sin deducir y de las dos entradas."""
    validar_datos(df)
    if len(df) != 12:
        raise ValueError("El segundo corte debe conservar los 12 registros originales.")
    if set(etiquetas.columns) != {"radicado", "prioridad_alta", "justificacion"}:
        raise ValueError("Las etiquetas deben incluir radicado, prioridad_alta y justificacion.")
    if (
        etiquetas.isna().any().any()
        or etiquetas["radicado"].duplicated().any()
        or set(etiquetas["radicado"]) != set(df["radicado"])
        or not pd.api.types.is_integer_dtype(etiquetas["prioridad_alta"])
        or not etiquetas["prioridad_alta"].isin([0, 1]).all()
        or not etiquetas["justificacion"].map(
            lambda valor: isinstance(valor, str) and bool(valor.strip())
        ).all()
    ):
        raise ValueError("Se requiere una etiqueta binaria justificada por cada radicado.")

    df_limpio = limpiar_datos(df)
    df_limpio = df_limpio.merge(
        etiquetas[["radicado", "prioridad_alta"]],
        on="radicado", how="left", validate="one_to_one", sort=False,
    )
    df_ml = df_limpio[[
        "dias_desde_radicacion", "longitud_descripcion", "prioridad_alta",
    ]].copy()
    resumen = pd.DataFrame([
        {"etapa": etapa, "filas": datos.shape[0], "columnas": datos.shape[1],
         "nulos": int(datos.isna().sum().sum())}
        for etapa, datos in [("antes", df), ("despues", df_limpio)]
    ])
    return df_limpio, df_ml, resumen


def ejecutar_segundo_corte(df):
    etiquetas = pd.read_csv(BASE_DIR / "data" / "etiquetas_prioridad.csv")
    df_limpio, df_ml, resumen = preparar_segundo_corte(df, etiquetas)
    print("\nDATASET LIMPIO:")
    print("shape:", df_limpio.shape)
    df_limpio.info()
    print("\nANTES / DESPUÉS:")
    print(resumen.to_string(index=False))
    print("\nDISTRIBUCIÓN DE prioridad_alta (0 = media/baja, 1 = alta):")
    conteos = df_limpio["prioridad_alta"].value_counts().reindex([0, 1], fill_value=0)
    print(pd.DataFrame({"registros": conteos, "porcentaje": conteos / len(df_limpio) * 100}))
    df_limpio.to_csv(BASE_DIR / "data" / "pqrs_limpias_segundo_corte.csv", index=False)
    df_ml.to_csv(BASE_DIR / "data" / "pqrs_ml_segundo_corte.csv", index=False)
    resumen.to_csv(BASE_DIR / "data" / "resumen_limpieza_segundo_corte.csv", index=False)
    print("\nExportados: pqrs_limpias_segundo_corte.csv, pqrs_ml_segundo_corte.csv "
          "y resumen_limpieza_segundo_corte.csv en data/.")


def visualizar_segundo_corte():
    """Lee el CSV limpio y genera únicamente las figuras del requisito C."""
    df = pd.read_csv(BASE_DIR / "data" / "pqrs_limpias_segundo_corte.csv")
    columnas_originales = [
        "radicado", "tipo", "estado", "dias_desde_radicacion", "asunto", "descripcion",
    ]
    if set(df.columns) != set(columnas_originales + ["longitud_descripcion", "prioridad_alta"]):
        raise ValueError("El dataset limpio debe tener las ocho columnas del segundo corte.")
    validar_datos(df[columnas_originales])
    if (
        len(df) != 12
        or not pd.api.types.is_integer_dtype(df["longitud_descripcion"])
        or not df["longitud_descripcion"].eq(df["descripcion"].str.len()).all()
        or not pd.api.types.is_integer_dtype(df["prioridad_alta"])
        or set(df["prioridad_alta"]) != {0, 1}
    ):
        raise ValueError("Se requieren los 12 casos limpios, longitudes válidas y ambas clases binarias.")

    visualizar_datos(df, segundo_corte=True)
    dias = df["dias_desde_radicacion"]
    tipos = df["tipo"].value_counts()
    clases = df["prioridad_alta"].value_counts()
    informe = (
        "# Segundo corte - Requisito C: visualizaciones\n\n"
        "Fuente: `data/pqrs_limpias_segundo_corte.csv` (12 casos sintéticos).\n"
        "Se reutilizan los gráficos de Seaborn de Clase 7, sin sobrescribirlos.\n\n"
        "## 1. Distribución de días desde la radicación\n\n"
        "![Distribución de días](histograma_dias_pqrs.png)\n\n"
        f"La antigüedad va de {dias.min()} a {dias.max()} días, con mediana de {dias.median():g} días.\n"
        "La dispersión de esta entrada respalda revisar su escala y considerar una normalización futura; "
        "el histograma no determina la prioridad.\n\n"
        "## 2. Cantidad de PQRS por tipo\n\n"
        "![Cantidad de PQRS por tipo](pqrs_por_tipo.png)\n\n"
        f"El tipo más frecuente es {tipos.index[0]}, con {tipos.iloc[0]} de {len(df)} casos "
        f"({tipos.iloc[0] / len(df):.1%}); las categorías tienen una representación desigual.\n"
        "Esto respalda explicitar la cobertura limitada de escenarios; el tipo se conserva como contexto "
        "y no se añade a las dos entradas numéricas elegidas.\n\n"
        "## 3. Entradas numéricas y prioridad alta\n\n"
        "![Días y longitud según prioridad](antiguedad_vs_descripcion.png)\n\n"
        f"Cada punto relaciona días y caracteres con su etiqueta (0: {clases[0]} casos; 1: {clases[1]}), "
        "distinguida por color y marcador.\n"
        "Respalda examinar conjuntamente ambas entradas frente a las anotaciones semánticas; "
        "la inspección visual no demuestra separabilidad lineal ni capacidad predictiva.\n\n"
        "Las etiquetas son académicas y subjetivas; 12 registros no permiten generalizar resultados.\n"
    )
    ruta = BASE_DIR / "informes" / "segundo_corte" / "interpretaciones.md"
    ruta.write_text(informe, encoding="utf-8")
    print(f"Interpretaciones guardadas: {ruta}")


def main():
    parser = argparse.ArgumentParser(description="Preparación académica de datos PQRS")
    modos = parser.add_mutually_exclusive_group()
    modos.add_argument("--segundo-corte", action="store_true",
                       help="Exporta datos y etiquetas del segundo corte sin alterar Clase 7")
    modos.add_argument("--visualizaciones-segundo-corte", action="store_true",
                       help="Lee el dataset limpio y exporta gráficos e interpretaciones del requisito C")
    args = parser.parse_args()
    if args.visualizaciones_segundo_corte:
        visualizar_segundo_corte()
        return
    print("=" * 60)
    print("PREPARACIÓN DE DATOS DE PQRS")
    print("=" * 60)

    df = cargar_datos(BASE_DIR / "data" / "pqrs.csv")

    if df is None:
        return

    explorar_datos(df)

    if args.segundo_corte:
        ejecutar_segundo_corte(df)
        return

    df_limpio = limpiar_datos(df)

    visualizar_datos(df_limpio)

    df_ml = preparar_ml(df_limpio)
    df_ml.to_csv(BASE_DIR / "data" / "pqrs_preparadas_ml.csv", index=False)

    print("\nArchivo creado: data/pqrs_preparadas_ml.csv")
    print("Proceso completado.")


if __name__ == "__main__":
    main()
