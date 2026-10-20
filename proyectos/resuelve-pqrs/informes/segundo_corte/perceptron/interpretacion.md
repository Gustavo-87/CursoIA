# Requisito D - Perceptrón con activación sigmoide

## Implementación y ejecución

Se utiliza exclusivamente `data/pqrs_ml_segundo_corte.csv`, sin modificar sus
12 registros. Las entradas son `dias_desde_radicacion` y `longitud_descripcion`;
el objetivo es `prioridad_alta` (0 = media/baja; 1 = alta).

La neurona calcula `p = sigmoide(X_estandar @ w + b)` y predice 1 cuando
`p >= 0.5`. Es una neurona sigmoide equivalente a regresión logística binaria,
no el perceptrón clásico de activación escalón. Está implementada desde cero
con NumPy, sin Scikit-Learn. La pérdida logarítmica media se calcula de forma
estable desde los logits: `mean(logaddexp(0, z) - y*z)`.
El gradiente por lotes usa `dw = X_estandar.T @ (p-y) / n` y `db = mean(p-y)`;
se actualiza cada parámetro restando la tasa multiplicada por su gradiente.

Las dos entradas se estandarizan con `(X-media)/desviacion` y `ddof=0`, usando
solo los datos de entrenamiento (los 12 casos, sin partición de validación):

| Entrada | Media | Desviación estándar |
|---|---:|---:|
| Días desde radicación | 56.5 | 48.83048911 |
| Longitud de descripción | 74.33333333 | 9.98610145 |

Se usan 10000 épocas, tasa 0.1 e inicialización `w1=w2=b=0`. No hay muestreo
aleatorio ni dependencia de una semilla.

Desde la raíz de **CursoIA**:

```bash
docker compose run --rm -e MPLBACKEND=Agg python python proyectos/resuelve-pqrs/src/perceptron_proyecto.py
docker compose run --rm -e MPLBACKEND=Agg python python -m unittest discover -s proyectos/resuelve-pqrs/tests -v
```

## Resultados en Docker (Python 3.13.16)

| Resultado | Valor |
|---|---:|
| w1 (días estandarizados) | 1.5041201103 |
| w2 (longitud estandarizada) | 1.9560568515 |
| b | -1.1298185501 |
| Pérdida inicial | 0.6931471806 |
| Pérdida final | 0.5270863308 |
| Exactitud de entrenamiento | 9/12 = 75.00 % |

Predicciones en el orden del CSV: `[1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0]`.

## Gráficos e interpretación

![Curva de aprendizaje](curva_aprendizaje.png)

La pérdida disminuye desde 0.693147 hasta 0.527086 y se estabiliza.
Esto verifica el aprendizaje por gradiente en entrenamiento, pero no demuestra
exactitud fuera de la muestra ni ausencia de errores de clasificación.

![Frontera de decisión](frontera_decision.png)

La línea negra corresponde a `p=0.5` (logit cero); los fondos indican la región
predicha y los puntos muestran las etiquetas académicas reales. Los ejes están
en días y caracteres originales; la malla se transforma con las mismas medias
y desviaciones empleadas al entrenar.

Ambos pesos son **positivos**: aumentar días o longitud, manteniendo la otra
entrada fija, aumenta la probabilidad estimada de prioridad alta. Son efectos
condicionales de este ajuste, no relaciones causales ni reglas de etiquetado.
El sesgo negativo desplaza hacia abajo el logit en el punto de entradas medias.

### Separabilidad lineal

El conjunto **no es linealmente separable** con estas dos entradas. El caso
de clase 0 `(48, 81)` está dentro del triángulo cuyos vértices son los casos
de clase 1 `(2, 89)`, `(18, 88)` y `(155, 60)`: es su combinación convexa con
coeficientes aproximados `0.38263666`, `0.35369775` y `0.26366559`.
Una recta no puede separar ese punto de los tres vértices. Esta propiedad se
conserva al estandarizar; se verifica numéricamente en las pruebas. La exactitud
menor al 100 % por sí sola no habría demostrado falta de separabilidad.

## Verificaciones y limitaciones

- Dos ejecuciones completas en Docker produjeron la misma salida numérica y
  los mismos SHA-256 para ambos PNG. Se verifica también mediante pruebas.
- El gradiente analítico coincide con diferencias finitas; la sigmoide y la
  pérdida soportan logits extremos sin desbordamiento ni `log(0)`.
- Las pruebas verifican estandarización, descenso de pérdida, parámetros,
  exactitud, errores de entrada y conservación del CSV. Pasaron 19 pruebas
  (7 del modelo y 12 de las etapas anteriores).
- Los CSV y gráficos de etapas anteriores conservaron sus SHA-256.

La exactitud es exclusivamente de entrenamiento: no se ha medido generalización
con datos independientes. Solo hay 12 casos sintéticos, con clases desbalanceadas
(8/4) y etiquetas subjetivas. Días y longitud no capturan la semántica del riesgo
que motivó dichas etiquetas. Las probabilidades no están validadas ni calibradas
para uso operativo. La igualdad exacta se comprobó en el mismo entorno Docker;
otras versiones o plataformas pueden introducir diferencias de redondeo.
