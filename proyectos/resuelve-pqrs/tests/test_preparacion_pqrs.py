import contextlib
import io
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

import pandas as pd

BASE_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(BASE_DIR / "src"))
from preparacion_pqrs import preparar_segundo_corte


class PreparacionSegundoCorteTest(unittest.TestCase):
    def setUp(self):
        self.df = pd.read_csv(BASE_DIR / "data" / "pqrs.csv")
        self.etiquetas = pd.read_csv(BASE_DIR / "data" / "etiquetas_prioridad.csv")
        salida = contextlib.redirect_stdout(io.StringIO())
        salida.__enter__()
        self.addCleanup(salida.__exit__, None, None, None)

    def preparar(self, df=None, etiquetas=None):
        return preparar_segundo_corte(
            self.df if df is None else df,
            self.etiquetas if etiquetas is None else etiquetas,
        )

    def test_conserva_registros_originales_y_solo_agrega_dos_columnas(self):
        original = self.df.copy(deep=True)
        limpio, ml, resumen = self.preparar()
        pd.testing.assert_frame_equal(self.df, original)
        pd.testing.assert_frame_equal(limpio[original.columns], original)
        self.assertEqual(limpio.shape, (12, 8))
        self.assertEqual(ml.shape, (12, 3))
        self.assertEqual(list(ml), [
            "dias_desde_radicacion", "longitud_descripcion", "prioridad_alta",
        ])
        self.assertTrue(all(pd.api.types.is_numeric_dtype(ml[c]) for c in ml))
        self.assertEqual(resumen["filas"].tolist(), [12, 12])
        self.assertEqual(resumen["columnas"].tolist(), [6, 8])
        self.assertEqual(resumen["nulos"].tolist(), [0, 0])
        self.assertEqual(limpio["longitud_descripcion"].tolist(),
                         original["descripcion"].str.len().tolist())
        self.assertEqual(limpio["prioridad_alta"].value_counts().to_dict(), {0: 8, 1: 4})
        self.assertEqual(set(limpio.loc[limpio.prioridad_alta == 1, "radicado"]),
                         {"PQR-0001", "PQR-0004", "PQR-0008", "PQR-0012"})

    def test_etiquetas_por_radicado_no_por_orden_o_entradas(self):
        df = self.df.copy()
        df["dias_desde_radicacion"] = 0
        df["descripcion"] = "Texto de longitud idéntica."
        limpio, _, _ = self.preparar(df, self.etiquetas.iloc[::-1])
        self.assertEqual(limpio["prioridad_alta"].tolist(),
                         self.etiquetas["prioridad_alta"].tolist())

    def test_conversion_de_dias_textuales_sin_imputacion(self):
        df = self.df.copy()
        df["dias_desde_radicacion"] = df["dias_desde_radicacion"].astype(str)
        limpio, _, _ = self.preparar(df)
        pd.testing.assert_series_equal(limpio["dias_desde_radicacion"],
                                       self.df["dias_desde_radicacion"])

    def test_rechaza_dias_inconsistentes(self):
        for valor in [None, "error", -1, 1.5, float("inf"), True]:
            with self.subTest(valor=valor), self.assertRaises(ValueError):
                df = self.df.copy()
                df["dias_desde_radicacion"] = df["dias_desde_radicacion"].astype(object)
                df.loc[0, "dias_desde_radicacion"] = valor
                self.preparar(df)

    def test_rechaza_textos_o_categorias_invalidas(self):
        for columna, valor in [
            ("descripcion", None), ("descripcion", " "), ("descripcion", 123),
            ("tipo", "Otro"), ("estado", "Desconocido"),
        ]:
            with self.subTest(columna=columna, valor=valor), self.assertRaises(ValueError):
                df = self.df.copy()
                df[columna] = df[columna].astype(object)
                df.loc[0, columna] = valor
                self.preparar(df)

    def test_rechaza_duplicados_cambios_de_esquema_o_cantidad(self):
        for df in [
            pd.concat([self.df, self.df.iloc[[0]]], ignore_index=True),
            self.df.assign(radicado="PQR-0001"), self.df.iloc[:-1],
            self.df.drop(columns="descripcion"),
        ]:
            with self.subTest(shape=df.shape), self.assertRaises(ValueError):
                self.preparar(df)

    def test_rechaza_etiquetas_invalidas(self):
        variantes = [self.etiquetas.iloc[:-1], self.etiquetas.assign(radicado="PQR-0001")]
        for columna, valor in [("prioridad_alta", 2), ("prioridad_alta", None),
                               ("justificacion", " "), ("radicado", "PQR-0099")]:
            etiquetas = self.etiquetas.copy()
            etiquetas[columna] = etiquetas[columna].astype(object)
            etiquetas.loc[0, columna] = valor
            variantes.append(etiquetas)
        for etiquetas in variantes:
            with self.subTest(), self.assertRaises(ValueError):
                self.preparar(etiquetas=etiquetas)

    def test_cli_exporta_desde_otro_cwd_sin_sobrescribir_original(self):
        with tempfile.TemporaryDirectory() as temporal:
            proyecto = Path(temporal)
            (proyecto / "src").mkdir()
            (proyecto / "data").mkdir()
            shutil.copy(BASE_DIR / "src" / "preparacion_pqrs.py", proyecto / "src")
            for nombre in ["pqrs.csv", "etiquetas_prioridad.csv"]:
                shutil.copy(BASE_DIR / "data" / nombre, proyecto / "data")
            original = (proyecto / "data" / "pqrs.csv").read_bytes()
            resultado = subprocess.run(
                [sys.executable, str(proyecto / "src" / "preparacion_pqrs.py"),
                 "--segundo-corte"], cwd="/", capture_output=True, text=True,
                check=True,
            )
            self.assertIn("AUDITORÍA DE CALIDAD", resultado.stdout)
            self.assertEqual(original, (proyecto / "data" / "pqrs.csv").read_bytes())
            self.assertEqual(pd.read_csv(proyecto / "data" / "pqrs_limpias_segundo_corte.csv").shape,
                             (12, 8))
            self.assertEqual(pd.read_csv(proyecto / "data" / "pqrs_ml_segundo_corte.csv").shape,
                             (12, 3))
            self.assertTrue((proyecto / "data" / "resumen_limpieza_segundo_corte.csv").is_file())
            self.assertFalse((proyecto / "data" / "pqrs_preparadas_ml.csv").exists())
            self.assertEqual(list(proyecto.glob("*.png")), [])


if __name__ == "__main__":
    unittest.main()
