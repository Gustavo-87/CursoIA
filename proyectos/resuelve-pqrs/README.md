# Integración de IA para la Gestión de PQRS en Conjuntos Residenciales de Cartago, Valle del Cauca

## Problemática

Los administradores de conjuntos residenciales deben atender constantemente peticiones, quejas, reclamos y sugerencias (PQRS) presentadas por los residentes. La redacción de respuestas claras y apropiadas, la selección de formatos para cada caso y el seguimiento de las solicitudes pueden requerir mucho tiempo y generar dificultades en la gestión administrativa.

La plataforma Resuelve permite registrar y hacer seguimiento a las PQRS. Sin embargo, los administradores todavía deben analizar cada solicitud y preparar manualmente gran parte de las respuestas y comunicaciones.

La incorporación de inteligencia artificial en Resuelve permitirá ofrecer ideas de redacción, sugerir plantillas de respuesta y brindar apoyo durante la gestión de las PQRS. De esta manera, los administradores de conjuntos residenciales en Cartago, Valle del Cauca, podrán preparar respuestas con mayor agilidad, mantener una comunicación más clara y organizar mejor la atención de las solicitudes.

## Objetivo

Integrar un asistente de inteligencia artificial en la plataforma Resuelve que, a partir del contenido de cada PQRS, genere ideas de redacción, sugiera plantillas de respuesta y apoye al administrador durante el seguimiento de la solicitud, con el fin de agilizar su gestión y mejorar la claridad de las comunicaciones dirigidas a los residentes.

## Datos

Para este primer avance se utiliza un archivo CSV con 12 datos sintéticos, adaptados de los casos de demostración de Resuelve. La plataforma aún no está desplegada en conjuntos residenciales y, por tanto, no cuenta con registros operativos de residentes.

El conjunto de datos representará solicitudes habituales presentadas por residentes y contendrá campos como:

- Número de radicado.
- Asunto de la solicitud.
- Tipo de PQRS.
- Estado.
- Días transcurridos desde la radicación.
- Descripción de la solicitud.

El uso de datos sintéticos permite representar escenarios realistas, desarrollar el análisis inicial y proteger la información personal y confidencial de los residentes.

## Análisis exploratorio de datos

El programa carga los registros del archivo `data/pqrs.csv` como una lista de diccionarios. Posteriormente, utiliza NumPy para analizar la columna `dias_desde_radicacion` y calcular:

- Promedio.
- Valor máximo.
- Valor mínimo.
- Desviación estándar.

También utiliza Matplotlib para generar un gráfico de barras con la cantidad de PQRS registradas por cada tipo.

## Resultados

El análisis de los 12 registros sintéticos produjo los siguientes resultados:

- Promedio de días desde la radicación: 56.50 días.
- Máximo de días desde la radicación: 155 días.
- Mínimo de días desde la radicación: 2 días.
- Desviación estándar: 48.83 días.

## Hallazgos

1. El reclamo es el tipo de PQRS más frecuente, con 4 de los 12 registros analizados.
2. El 50 % de las PQRS se encuentra en estado radicada o en revisión, lo cual representa 6 solicitudes que todavía requieren gestión administrativa.

## Visualización

El siguiente gráfico presenta la cantidad de solicitudes registradas por cada tipo de PQRS:

![Cantidad de PQRS por tipo](grafico_pqrs.png)

La visualización permite identificar que los reclamos son el tipo de solicitud con mayor frecuencia dentro del conjunto de datos analizado.

## Requisitos

- Python 3.
- NumPy.
- Matplotlib.

Las librerías necesarias se encuentran registradas en `requirements.txt`.

## Ejecución

Desde la carpeta principal del proyecto, instalar las dependencias:

```bash
python -m pip install -r requirements.txt
```

Luego ejecutar el análisis:

```bash
python src/analisis_pqrs.py
```

## Estructura del proyecto

```text
ia-gestion-pqrs/
├── data/
│   └── pqrs.csv
├── src/
│   └── analisis_pqrs.py
├── .gitignore
├── grafico_pqrs.png
├── README.md
└── requirements.txt
```

## Tecnologías utilizadas

- Python 3.
- CSV para almacenar los datos sintéticos.
- NumPy para los cálculos estadísticos.
- Matplotlib para la visualización.
- Git y GitHub para el control de versiones.
- Visual Studio Code como entorno de desarrollo.

## Próximos pasos

En los siguientes avances se plantea integrar inteligencia artificial en Resuelve para:

- Generar ideas de redacción para las respuestas a las PQRS.
- Sugerir plantillas según el tipo de solicitud.
- Apoyar al administrador durante la gestión y seguimiento de cada caso.
- Evaluar las respuestas sugeridas antes de incorporarlas a la plataforma.

## Clase 7 - Preparación de Datos

Para la actividad independiente se utilizó el archivo `data/pqrs.csv`, compuesto por 12 registros sintéticos relacionados con la gestión de PQRS en conjuntos residenciales.

### Exploración con Pandas

El script `src/preparacion_pqrs.py` carga los datos con `pd.read_csv()` y muestra:

- Las primeras cinco filas con `df.head()`.
- La estructura y tipos de datos con `df.info()`.
- Las estadísticas descriptivas con `df.describe()`.
- Los valores nulos por columna con `df.isnull().sum()`.

El conjunto tiene 12 filas y 6 columnas. Se identificó que no existen valores nulos en ninguna de sus columnas.

### Limpieza y preparación

La columna `dias_desde_radicacion` se convierte a formato numérico. El código incluye un manejo condicional: si en futuros registros aparecen valores nulos en esta columna, se reemplazarán mediante la mediana. En los datos analizados no fue necesario aplicar esa imputación.

Las variables categóricas `tipo` y `estado` se codificaron con One-Hot Encoding mediante `pd.get_dummies()`. Esto crea columnas numéricas que pueden usarse en un futuro modelo de aprendizaje automático.

También se creó la columna derivada `longitud_descripcion`, que cuenta los caracteres de la descripción de cada PQRS. Esta variable permite explorar si la extensión del texto presenta alguna relación con la antigüedad de la solicitud.

El resultado se guarda en `data/pqrs_preparadas_ml.csv`. Esta copia contiene datos numéricos preparados para un futuro ejercicio de Machine Learning; todavía no se entrena un modelo, ya que el conjunto tiene únicamente 12 registros sintéticos.

### Visualizaciones con Seaborn

#### Distribución de días desde la radicación

![Histograma de días desde la radicación](histograma_dias_pqrs.png)

Cinco de las doce PQRS tienen entre 2 y 25 días desde su radicación. Sin embargo, existen solicitudes con 130 y 155 días, lo cual muestra diferencias importantes en la antigüedad de los casos y la necesidad de hacer seguimiento.

#### Cantidad de PQRS por tipo

![Cantidad de PQRS por tipo](pqrs_por_tipo.png)

Los reclamos son el tipo más frecuente, con 4 de 12 registros (33,3 %). En este conjunto sintético, este hallazgo puede orientar la creación futura de plantillas e ideas de redacción para reclamos.

#### Antigüedad y longitud de la descripción

![Antigüedad y longitud de la descripción](antiguedad_vs_descripcion.png)

No se observa una relación directa entre los días desde la radicación y la longitud de la descripción. Por ello, una futura solución de IA debería considerar principalmente el contenido y tipo de la PQRS, no solamente su antigüedad.

## Clase 8 - Neurona Artificial y Compuertas Lógicas

En esta actividad se implementó una neurona artificial o perceptrón simple en Python. La neurona calcula una suma ponderada de las entradas y aplica una función escalón para producir una salida de 0 o 1.

Primero se implementó la compuerta AND en `src/neurona_and.py`. Con los parámetros iniciales `w1 = 0.1`, `w2 = 0.1` y `b = 0.0`, la neurona redujo su error hasta cero y aprendió la compuerta en 3 épocas.

![Evolución del error de AND](evolucion_error.png)

También se implementaron las compuertas OR y NOT en `src/neuronas_logicas.py`.

- La compuerta OR aprendió en 2 épocas.
- La compuerta NOT aprendió en 4 épocas.
- En los tres casos se utilizó una tasa de aprendizaje de 0.1; no fue necesario modificarla porque el error llegó a cero.

![Evolución del error de OR](evolucion_error_or.png)

![Evolución del error de NOT](evolucion_error_not.png)

La diferencia principal entre AND y OR está en su salida esperada. AND solo devuelve 1 cuando ambas entradas son 1; OR devuelve 1 cuando al menos una entrada es 1.

La compuerta XOR no puede ser aprendida por una sola neurona o perceptrón simple porque sus resultados no son separables mediante una sola frontera de decisión lineal. Para aprender XOR se requiere una red con más de una neurona, por ejemplo una capa oculta.

## Avance 2

El segundo corte reúne la preparación de datos, tres visualizaciones Seaborn
y una neurona sigmoide implementada con NumPy. Todo el trabajo permanece
separado de Resuelve ERP y conserva los ejercicios y resultados de Clase 7 y 8.

Resumen: 12 registros originales sin ampliar, clases 0/1 con distribución 8/4,
dos entradas estandarizadas y exactitud de entrenamiento del 75 % (9/12).
Los detalles y comandos de preparación y visualización aparecen a continuación;
el modelo y sus resultados se describen en el apartado «Requisito D».

### Preparación para clasificación binaria

Se reutilizan exclusivamente los 12 registros de `data/pqrs.csv`. El modo
`--segundo-corte` de `src/preparacion_pqrs.py` conserva el flujo anterior de
Clase 7 (ejecución sin argumentos), sus gráficos y su CSV preparado.

### Variable objetivo y criterio académico

`prioridad_alta`: **1 = alta**, **0 = media o baja**. Las anotaciones manuales
están en `data/etiquetas_prioridad.csv`, con una justificación por radicado.
Se basan en el asunto y el contenido del incidente: alta cuando se describe
un riesgo físico o de daño material que amerita atención preventiva; media/baja
para trámites, mejoras o afectaciones sin ese riesgo explícito. No se calculan
mediante umbrales de días, longitud ni estado. Representan la gravedad del
incidente **al reportarse**, no una cola de atención actual: por eso PQR-0012
es alta aunque ahora figure cerrada.

| Radicado | Etiqueta | Motivo resumido |
|---|---:|---|
| PQR-0001 | 1 | Oscuridad en pasillo: riesgo de caídas. |
| PQR-0002 | 0 | Ruido: convivencia sin peligro físico explícito. |
| PQR-0003 | 0 | Trámite documental. |
| PQR-0004 | 1 | Filtración: riesgo de daño material. |
| PQR-0005 | 0 | Propuesta de bicicletero. |
| PQR-0006 | 0 | Autorización de acompañante sin emergencia descrita. |
| PQR-0007 | 0 | Apertura remota defectuosa sin bloqueo de salida descrito. |
| PQR-0008 | 1 | Rama seca sobre juegos: riesgo para niños. |
| PQR-0009 | 0 | Mejora de señalización. |
| PQR-0010 | 0 | Reclamación contable. |
| PQR-0011 | 0 | Reserva de espacio. |
| PQR-0012 | 1 | Agua en piso: riesgo de resbalones al reportarse. |

Estas etiquetas son supuestos académicos, no prioridades oficiales ni dictámenes
técnicos. No se infieren daños estructurales ni emergencias ausentes del texto.
Las decisiones subjetivas requieren validación experta si se usan fuera del curso.

### Auditoría, limpieza y exportaciones

Pandas muestra `shape`, `info()`, estadísticas, nulos, duplicados completos y
de radicado, tipos no numéricos en días, textos vacíos/no textuales, categorías
desconocidas y días no finitos, negativos o fraccionarios. Solo se convierten
días textuales válidos a números si es necesario. Ante inconsistencias se detiene
la exportación: no se imputan valores ni se eliminan registros automáticamente.
En estos 12 casos no se necesitan correcciones de valores ni eliminación de filas.

Se agrega `longitud_descripcion` (número de caracteres del texto original) y se
incorpora la etiqueta mediante unión uno a uno por `radicado`. Se exportan:

- `data/pqrs_limpias_segundo_corte.csv`: seis columnas originales, longitud y objetivo.
- `data/pqrs_ml_segundo_corte.csv`: solo `dias_desde_radicacion`,
  `longitud_descripcion` (entradas numéricas) y `prioridad_alta` (objetivo).
  No incluye identificadores, justificaciones ni categorías como entradas.
- `data/resumen_limpieza_segundo_corte.csv`: tabla antes/después del dataset limpio.

| Etapa | Filas | Columnas | Nulos |
|---|---:|---:|---:|
| Antes | 12 | 6 | 0 |
| Después | 12 | 8 | 0 |

Distribución: clase **0: 8 (66,67 %)**; clase **1: 4 (33,33 %)**. Las dos columnas
nuevas son derivación y anotación, no correcciones de datos originales.

### Verificación en Docker

Desde la raíz de **CursoIA**, usando su servicio Docker único y Python 3.13:

```bash
docker compose build
docker compose run --rm -e MPLBACKEND=Agg python python proyectos/resuelve-pqrs/src/preparacion_pqrs.py --segundo-corte
docker compose run --rm -e MPLBACKEND=Agg python python -m unittest discover -s proyectos/resuelve-pqrs/tests -v
```

Las pruebas incluyen preservación de filas/columnas originales, conteos,
longitudes, asociación de etiquetas por radicado (independiente del orden y
de las entradas), conversión numérica, rechazo de inconsistencias y exportación
desde otro directorio de trabajo. El CSV original y los resultados de Clase 7
no se sobrescriben; los archivos nuevos se regeneran al repetir el comando.

**Limitaciones:** muestra sintética diminuta, clases desbalanceadas y etiquetas
subjetivas no validadas con expertos. Días y longitud no capturan la semántica
del riesgo que justifica las etiquetas; no se garantiza separabilidad lineal ni
capacidad predictiva. Esta fase no entrena un perceptrón ni modifica Resuelve ERP.

### Requisito C - Visualizaciones del segundo corte

Se reutilizan el histograma de antigüedad, el conteo por tipo y la dispersión
de días frente a longitud de descripción. En esta última, el color y el marcador
identifican `prioridad_alta` (0 = media/baja; 1 = alta). Los tres tienen título
y ejes explícitos. El histograma usa seis intervalos sin KDE para no sugerir
una densidad continua estimada a partir de solo 12 casos.

Desde la raíz de **CursoIA**:

```bash
docker compose run --rm -e MPLBACKEND=Agg python python proyectos/resuelve-pqrs/src/preparacion_pqrs.py --visualizaciones-segundo-corte
```

Este modo lee exclusivamente `data/pqrs_limpias_segundo_corte.csv`, valida sus
12 casos y no prepara ni sobrescribe datasets. Si falta el CSV limpio, primero
debe ejecutarse `--segundo-corte`. Los dos modos son mutuamente excluyentes.

Los PNG se guardan en `informes/segundo_corte/`:

- `histograma_dias_pqrs.png`: rango de 2–155 días y mediana de 40 días;
  respalda revisar la escala de la entrada, no inferir prioridad por antigüedad.
- `pqrs_por_tipo.png`: Reclamo es el tipo más frecuente (4/12);
  respalda reconocer la cobertura desigual sin añadir tipo como entrada.
- `antiguedad_vs_descripcion.png`: relaciona las dos entradas con las clases
  (8 media/baja y 4 alta); respalda examinarlas conjuntamente, sin afirmar
  separabilidad lineal ni rendimiento predictivo.

Cada figura se acompaña de una interpretación de dos líneas en
[`informes/segundo_corte/interpretaciones.md`](informes/segundo_corte/interpretaciones.md).
Los gráficos históricos de la raíz y los ejercicios anteriores se conservan.

### Requisito D - Perceptrón sigmoide del proyecto

`src/perceptron_proyecto.py` utiliza únicamente `data/pqrs_ml_segundo_corte.csv`.
Estandariza las dos entradas con media y desviación poblacional (`ddof=0`)
calculadas sobre los 12 casos de entrenamiento. La activación es sigmoide,
la pérdida es logarítmica y se minimiza mediante descenso del gradiente por
lotes, implementado desde cero con NumPy, sin Scikit-Learn.

Configuración reproducible: 10000 épocas, tasa 0.1, pesos y sesgo iniciales en
cero, sin muestreo aleatorio. Se predice clase 1 cuando `p >= 0.5`.

| Resultado | Valor |
|---|---:|
| w1 (días estandarizados) | 1.5041201103 |
| w2 (longitud estandarizada) | 1.9560568515 |
| b | -1.1298185501 |
| Pérdida inicial | 0.6931471806 |
| Pérdida final | 0.5270863308 |
| Exactitud de entrenamiento | 9/12 = 75 % |

Desde la raíz de **CursoIA**, después de preparar los datos:

```bash
docker compose run --rm -e MPLBACKEND=Agg python python proyectos/resuelve-pqrs/src/perceptron_proyecto.py
```

Gráficos del modelo:

![Curva de aprendizaje](informes/segundo_corte/perceptron/curva_aprendizaje.png)

![Frontera de decisión](informes/segundo_corte/perceptron/frontera_decision.png)

Los pesos positivos aumentan la probabilidad estimada al aumentar cada entrada,
manteniendo fija la otra; no implican causalidad. Las etiquetas no son
linealmente separables con estas dos entradas. El análisis, la justificación
geométrica y las limitaciones están en
[`perceptron/interpretacion.md`](informes/segundo_corte/perceptron/interpretacion.md).
El 75 % es exactitud de entrenamiento, no una evaluación de generalización.

### Verificación y trazabilidad del avance

Las 19 pruebas de `tests/` ya fueron ejecutadas con éxito en Docker, Python
3.13.16: 8 de preparación, 4 de visualizaciones y 7 del modelo. Cubren calidad
de datos, preservación de archivos, gráficos, gradiente analítico frente a
diferencias finitas, estabilidad numérica y reproducibilidad. Dos ejecuciones
del modelo produjeron la misma salida y los mismos SHA-256 de ambos gráficos.

Se versionan el código, cuatro CSV nuevos (etiquetas, limpio, entradas/objetivo
y resumen de limpieza), cinco gráficos del segundo corte, dos interpretaciones
y tres archivos de pruebas. Los datasets y gráficos anteriores no se eliminan.
El trabajo se organiza en commits de preparación, visualizaciones, modelo,
pruebas y documentación, sin reescribir el historial previo.

La publicación de estos commits en GitHub queda pendiente de autorización.
No se generan PDF ni video ni se incorporan funcionalidades adicionales.
