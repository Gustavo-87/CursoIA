import hashlib
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

import matplotlib.pyplot as plt
import numpy as np

BASE_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(BASE_DIR / "src"))
from perceptron_proyecto import (
    cargar_datos, entrenar, estandarizar, gradientes, perdida_logaritmica, sigmoide,
)


class PerceptronProyectoTest(unittest.TestCase):
    def setUp(self):
        self.X, self.y = cargar_datos(BASE_DIR / "data" / "pqrs_ml_segundo_corte.csv")

    def test_estandarizacion_y_reconstruccion(self):
        X, media, desviacion = estandarizar(self.X)
        np.testing.assert_allclose(X.mean(axis=0), 0, atol=1e-14)
        np.testing.assert_allclose(X.std(axis=0), 1, atol=1e-14)
        np.testing.assert_allclose(X * desviacion + media, self.X)
        with self.assertRaises(ValueError):
            estandarizar(np.ones((12, 2)))

    def test_sigmoide_y_perdida_estables(self):
        with np.errstate(over="raise", invalid="raise", divide="raise"):
            np.testing.assert_allclose(sigmoide(np.array([-1000, 0, 1000])), [0, 0.5, 1])
            self.assertAlmostEqual(perdida_logaritmica(self.y, np.zeros(12)), np.log(2))
            self.assertEqual(perdida_logaritmica(np.array([0, 1]), np.array([-1000, 1000])), 0)
            self.assertEqual(perdida_logaritmica(np.array([1, 0]), np.array([-1000, 1000])), 1000)

    def test_gradiente_con_diferencias_finitas(self):
        X, _, _ = estandarizar(self.X)
        w, b, paso = np.array([0.2, -0.3]), 0.1, 1e-6
        dw, db = gradientes(X, self.y, w, b)
        numericos = []
        for indice in range(2):
            delta = np.zeros(2)
            delta[indice] = paso
            numericos.append((
                perdida_logaritmica(self.y, X @ (w + delta) + b)
                - perdida_logaritmica(self.y, X @ (w - delta) + b)
            ) / (2 * paso))
        db_numerico = (perdida_logaritmica(self.y, X @ w + b + paso)
                       - perdida_logaritmica(self.y, X @ w + b - paso)) / (2 * paso)
        np.testing.assert_allclose(dw, numericos, rtol=1e-6, atol=1e-9)
        self.assertAlmostEqual(db, db_numerico, places=8)

    def test_entrenamiento_reproducible_sin_modificar_entradas(self):
        original = self.X.copy()
        X, _, _ = estandarizar(self.X)
        copia = X.copy()
        w, b, perdidas = entrenar(X, self.y)
        w2, b2, perdidas2 = entrenar(X, self.y)
        np.testing.assert_array_equal(w, w2)
        np.testing.assert_array_equal(perdidas, perdidas2)
        self.assertEqual(b, b2)
        self.assertEqual(len(perdidas), 10001)
        self.assertTrue((np.diff(perdidas) <= 1e-12).all())
        self.assertLess(perdidas[-1], perdidas[0])
        np.testing.assert_allclose(w, [1.50412011, 1.95605685], atol=1e-7)
        self.assertAlmostEqual(b, -1.1298185501, places=8)
        self.assertAlmostEqual(perdidas[-1], 0.5270863308, places=8)
        predicciones = (sigmoide(X @ w + b) >= 0.5).astype(int)
        self.assertEqual(int(np.sum(predicciones == self.y)), 9)
        np.testing.assert_array_equal(X, copia)
        np.testing.assert_array_equal(self.X, original)

    def test_testigo_de_no_separabilidad_lineal(self):
        # (48,81), clase 0, es combinación convexa estricta de tres casos de clase 1.
        triangulo = self.X[[0, 3, 11]]
        self.assertEqual(self.y[6], 0)
        np.testing.assert_array_equal(self.y[[0, 3, 11]], np.ones(3))
        coeficientes = np.linalg.solve(
            np.vstack((triangulo.T, np.ones(3))), np.append(self.X[6], 1),
        )
        self.assertTrue((coeficientes > 0).all())
        self.assertAlmostEqual(coeficientes.sum(), 1)
        np.testing.assert_allclose(coeficientes @ triangulo, self.X[6])

    def test_rechaza_datos_y_parametros_invalidos(self):
        X, _, _ = estandarizar(self.X)
        for opciones in [{"epocas": 0}, {"epocas": 1.5}, {"tasa_aprendizaje": 0},
                         {"tasa_aprendizaje": float("nan")}]:
            with self.subTest(opciones=opciones), self.assertRaises(ValueError):
                entrenar(X, self.y, **opciones)
        with self.assertRaises(ValueError):
            entrenar(X, np.full(12, 2))
        with tempfile.TemporaryDirectory() as temporal:
            ruta = Path(temporal) / "invalido.csv"
            for contenido in ["otra,columna\n1,2\n",
                              "dias_desde_radicacion,longitud_descripcion,prioridad_alta\n1,2,0\n"]:
                with self.subTest(contenido=contenido), self.assertRaises(ValueError):
                    ruta.write_text(contenido, encoding="utf-8")
                    cargar_datos(ruta)

    def test_cli_repetido_desde_otro_cwd_y_dos_graficos_validos(self):
        with tempfile.TemporaryDirectory() as temporal:
            proyecto = Path(temporal)
            (proyecto / "src").mkdir()
            (proyecto / "data").mkdir()
            shutil.copy(BASE_DIR / "src" / "perceptron_proyecto.py", proyecto / "src")
            csv = proyecto / "data" / "pqrs_ml_segundo_corte.csv"
            shutil.copy(BASE_DIR / "data" / csv.name, csv)
            contenido = csv.read_bytes()
            comando = [sys.executable, str(proyecto / "src" / "perceptron_proyecto.py")]
            hashes, salidas = [], []
            for _ in range(2):
                resultado = subprocess.run(comando, cwd="/", capture_output=True, text=True, check=True)
                salidas.append(resultado.stdout)
                graficos = sorted((proyecto / "informes" / "segundo_corte" / "perceptron").glob("*.png"))
                self.assertEqual({ruta.name for ruta in graficos},
                                 {"curva_aprendizaje.png", "frontera_decision.png"})
                hashes.append([hashlib.sha256(ruta.read_bytes()).hexdigest() for ruta in graficos])
                for ruta in graficos:
                    self.assertGreater(plt.imread(ruta).std(), 0)
            self.assertEqual(salidas[0], salidas[1])
            self.assertEqual(hashes[0], hashes[1])
            self.assertIn("9/12 = 75.00%", salidas[0])
            self.assertEqual(csv.read_bytes(), contenido)


if __name__ == "__main__":
    unittest.main()
