# Documentación de datos — `proyectos/resuelve-pqrs/data/`

Este documento describe los datos utilizados por el modelo final de PQRS:
su origen, diccionario de variables, generación, privacidad, distribución de
clases, limitaciones y condiciones de uso. El dataset principal del modelo es
[`pqrs_final_150.csv`](pqrs_final_150.csv).

## Dataset final: `pqrs_final_150.csv`

- **150 registros sintéticos** con 5 columnas.
- Generado de forma **determinista con semilla 42** por
  [`../src/generar_datos.py`](../src/generar_datos.py)
  (`numpy.random.default_rng(42)`); regenerarlo produce siempre el mismo
  archivo.
- Distribución de la variable objetivo `prioridad_alta`:
  **120 no alta (0)** y **30 alta (1)** — desbalance 80/20.

## Diccionario de variables

| Nombre | Tipo | Valores / rango | Descripción | Uso en el modelo |
|---|---|---|---|---|
| `dias_desde_radicacion` | Numérica (entero) | Generado uniformemente entre 1 y 150 (observado: 2–149) | Días transcurridos desde la radicación de la PQRS hasta la medición. | **Entrada numérica.** Se estandariza con `StandardScaler` dentro del `Pipeline`. |
| `longitud_descripcion` | Numérica (entero) | Generado uniformemente entre 30 y 300 (observado: 35–299) | Número de caracteres de la descripción de la solicitud. | **Entrada numérica.** Se estandariza con `StandardScaler` dentro del `Pipeline`. |
| `cantidad_adjuntos` | Numérica (entero) | 0 a 5 | Cantidad de archivos adjuntos asociados a la PQRS. | **Entrada numérica.** Se estandariza con `StandardScaler` dentro del `Pipeline`. |
| `tipo` | Categórica | Petición, Queja, Reclamo, Solicitud, Sugerencia | Tipo de solicitud registrada por el residente. | **Entrada categórica.** Se codifica con `OneHotEncoder` (tolerante a categorías no vistas en el entrenamiento). |
| `prioridad_alta` | Binaria (0/1) | 0 = no alta, 1 = alta | Etiqueta de prioridad de la PQRS. | **Variable objetivo (target).** No se utiliza como entrada. |

### Contrato de entrada único

Las cuatro variables predictoras se usan con estos mismos nombres y en este
orden tanto en [`../src/modelo_proyecto.py`](../src/modelo_proyecto.py)
(entrenamiento) como en [`../src/usar_modelo.py`](../src/usar_modelo.py)
(predicción):

1. `dias_desde_radicacion`
2. `longitud_descripcion`
3. `cantidad_adjuntos`
4. `tipo`

El orden de las columnas del CSV no afecta al modelo: los scripts seleccionan
las columnas por nombre siguiendo el contrato.

## Generación sintética y semilla

El dataset **no proviene de registros reales**: lo genera
[`../src/generar_datos.py`](../src/generar_datos.py) así:

- Las variables predictoras se generan de forma aleatoria y uniforme con
  `numpy.random.default_rng(42)` (días, longitud, cantidad de adjuntos y tipo).
- `prioridad_alta` se calcula con una **regla académica ponderada** sobre las
  **mismas variables predictoras** (días, longitud, adjuntos y tipo) más ruido
  gaussiano; se marca 1 para el 20 % de puntajes más altos (cuantil 0.80) y
  0 para el resto.

La semilla 42 garantiza que cualquier regeneración reproduzca exactamente el
mismo dataset.

## Privacidad

- El dataset **no contiene información personal real** de residentes ni de
  usuarios de Resuelve.
- Es **sintético y se creó para fines académicos** porque Resuelve aún no está
  desplegada en conjuntos residenciales y, por tanto, no dispone de registros
  operativos.
- No se recolectó, procesó ni almacenó información confidencial para construir
  estos datos; su uso elimina cualquier riesgo de exposición de datos personales.

## Distribución de clases

| Clase | Significado | Registros | Porcentaje |
|---|---|---:|---:|
| 0 | Prioridad no alta | 120 | 80 % |
| 1 | Prioridad alta | 30 | 20 % |

El desbalance implica que la exactitud por sí sola es engañosa: conviene
observar precisión, recall y F1 de la clase 1. En el conjunto de prueba el
recall de prioridad alta fue 0.333 (2 de 6 casos detectados).

## Circularidad metodológica (fuga de información)

`prioridad_alta` **fue generada a partir de las mismas variables predictoras**
que se usan para predecirla. Esto constituye una **circularidad o fuga
metodológica estructural**: el modelo solo puede aprender la regla artificial
con la que se creó la etiqueta, y sus métricas **no demuestran validez
predictiva real** sobre PQRS de la vida diaria. Esta condición debe declararse
en todo informe o demostración que use este dataset.

## Limitaciones

- Tamaño limitado: 150 registros sintéticos.
- Desbalance de clases: 120/30.
- Recall bajo de la clase prioridad alta en la evaluación (0.333).
- Probabilidades predichas no calibradas.
- Etiquetas artificiales sin validación de expertos en gestión de PQRS.
- Sin datos de otros años, zonas ni plataformas; no se conoce su comportamiento
  ante datos de otra distribución.

## Uso exclusivamente académico

Este dataset y los modelos entrenados con él son una **demostración académica**.
No son válidos para operación real ni para asignar prioridades a PQRS de
residentes sin datos reales suficientes, etiquetas verificadas por expertos y
una evaluación adicional independiente.

## Otros archivos del directorio (etapas anteriores)

| Archivo | Contenido | Etapa |
|---|---|---|
| `pqrs.csv` | 12 casos sintéticos iniciales (6 columnas). | Avance 1 |
| `etiquetas_prioridad.csv` | Etiquetas manuales `prioridad_alta` por radicado (12 casos). | Avance 2 |
| `pqrs_preparadas_ml.csv` | Dataset preparado con one-hot y `longitud_descripcion`. | Clase 7 |
| `pqrs_limpias_segundo_corte.csv` | Dataset limpio del segundo corte (12 casos, 8 columnas). | Avance 2 |
| `pqrs_ml_segundo_corte.csv` | Dos entradas numéricas + objetivo (12 casos); usado por el perceptrón. | Avance 2 |
| `resumen_limpieza_segundo_corte.csv` | Resumen antes/después de la limpieza. | Avance 2 |

Estos archivos se conservan por trazabilidad histórica; el modelo final usa
exclusivamente `pqrs_final_150.csv`.

## Regeneración del dataset final

Desde la raíz de **CursoIA**:

```bash
docker compose run --rm -e MPLBACKEND=Agg python python proyectos/resuelve-pqrs/src/generar_datos.py
```

La regeneración es determinista (semilla 42) y el archivo producido es
idéntico al versionado.
