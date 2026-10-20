import contextlib
import io
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

import matplotlib.pyplot as plt
import pandas as pd

BASE_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(BASE_DIR / "src"))
import preparacion_pqrs


class VisualizacionesSegundoCorteTest(unittest.TestCase):
    def setUp(self):
        self.df = pd.read_csv(BASE_DIR / "data" / "pqrs_limpias_segundo_corte.csv")

    def test_tres_graficos_con_ejes_y_objetivo_sin_modificar_datos(self):
        original = self.df.copy(deep=True)
        ejes = []

        def capturar_ejes(*args, **kwargs):
            ax = plt.gca()
            ejes.append((ax.get_title(), ax.get_xlabel(), ax.get_ylabel()))

        with tempfile.TemporaryDirectory() as temporal, \
                patch.object(preparacion_pqrs, "BASE_DIR", Path(temporal)), \
                patch.object(plt, "savefig", side_effect=capturar_ejes), \
                patch.object(preparacion_pqrs.sns, "scatterplot",
                             wraps=preparacion_pqrs.sns.scatterplot) as dispersion, \
                contextlib.redirect_stdout(io.StringIO()):
            preparacion_pqrs.visualizar_datos(self.df, segundo_corte=True)

        self.assertEqual(len(ejes), 3)
        self.assertTrue(all(titulo and x and y for titulo, x, y in ejes))
        self.assertEqual(dispersion.call_args.kwargs["x"], "dias_desde_radicacion")
        self.assertEqual(dispersion.call_args.kwargs["y"], "longitud_descripcion")
        self.assertEqual(dispersion.call_args.kwargs["hue"], "prioridad_alta")
        self.assertEqual(dispersion.call_args.kwargs["style"], "prioridad_alta")
        pd.testing.assert_frame_equal(self.df, original)
        self.assertEqual(plt.get_fignums(), [])

    def test_cli_lee_solo_dataset_limpio_y_preserva_resultados_anteriores(self):
        nombres = ["histograma_dias_pqrs.png", "pqrs_por_tipo.png",
                   "antiguedad_vs_descripcion.png"]
        with tempfile.TemporaryDirectory() as temporal:
            proyecto = Path(temporal)
            (proyecto / "src").mkdir()
            (proyecto / "data").mkdir()
            shutil.copy(BASE_DIR / "src" / "preparacion_pqrs.py", proyecto / "src")
            csv = proyecto / "data" / "pqrs_limpias_segundo_corte.csv"
            shutil.copy(BASE_DIR / "data" / csv.name, csv)
            contenido = csv.read_bytes()
            for nombre in nombres:
                (proyecto / nombre).write_bytes(b"grafico historico intacto")
            # No se copia pqrs.csv ni etiquetas: este modo debe leer solo el limpio.
            resultado = subprocess.run(
                [sys.executable, str(proyecto / "src" / "preparacion_pqrs.py"),
                 "--visualizaciones-segundo-corte"],
                cwd="/", capture_output=True, text=True, check=True,
            )
            self.assertIn("Interpretaciones guardadas", resultado.stdout)
            destino = proyecto / "informes" / "segundo_corte"
            self.assertEqual({ruta.name for ruta in destino.glob("*.png")}, set(nombres))
            for nombre in nombres:
                imagen = plt.imread(destino / nombre)
                self.assertGreater(imagen.shape[0], 0)
                self.assertGreater(imagen.std(), 0)
                self.assertEqual((proyecto / nombre).read_bytes(), b"grafico historico intacto")
            self.assertEqual(csv.read_bytes(), contenido)
            self.assertEqual(list((proyecto / "data").iterdir()), [csv])
            informe = (destino / "interpretaciones.md").read_text(encoding="utf-8")
            self.assertEqual(informe.count("## "), 3)
            for nombre in nombres:
                self.assertIn(f"({nombre})", informe)
            self.assertIn("0: 8 casos; 1: 4", informe)
            self.assertIn("40 días", informe)

    def test_rechaza_dataset_incompleto_o_inconsistente_antes_de_graficar(self):
        variantes = [self.df.iloc[:-1], self.df.drop(columns="prioridad_alta")]
        for columna, valor in [("prioridad_alta", 2), ("prioridad_alta", None),
                               ("longitud_descripcion", -1), ("dias_desde_radicacion", -1)]:
            df = self.df.copy()
            df.loc[0, columna] = valor
            variantes.append(df)
        with tempfile.TemporaryDirectory() as temporal, \
                patch.object(preparacion_pqrs, "BASE_DIR", Path(temporal)), \
                contextlib.redirect_stdout(io.StringIO()):
            directorio = Path(temporal)
            (directorio / "data").mkdir()
            csv = directorio / "data" / "pqrs_limpias_segundo_corte.csv"
            for df in variantes:
                with self.subTest(shape=df.shape), self.assertRaises(ValueError):
                    df.to_csv(csv, index=False)
                    preparacion_pqrs.visualizar_segundo_corte()
                self.assertFalse((directorio / "informes").exists())
            csv.unlink()
            with self.assertRaises(FileNotFoundError):
                preparacion_pqrs.visualizar_segundo_corte()

    def test_modos_excluyentes(self):
        with patch.object(sys, "argv", ["preparacion_pqrs.py", "--segundo-corte",
                                        "--visualizaciones-segundo-corte"]), \
                contextlib.redirect_stderr(io.StringIO()), \
                self.assertRaises(SystemExit) as error:
            preparacion_pqrs.main()
        self.assertEqual(error.exception.code, 2)


if __name__ == "__main__":
    unittest.main()
