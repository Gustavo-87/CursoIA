# Curso de Inteligencia Artificial

Repositorio académico para desarrollar las actividades del curso de Inteligencia Artificial y el proyecto **Resuelve**, una propuesta orientada al análisis de Peticiones, Quejas, Reclamos y Sugerencias (PQRS).

## Objetivo del proyecto

Aplicar Python, análisis de datos e Inteligencia Artificial para procesar información de PQRS, identificar patrones y generar resultados que apoyen su gestión y priorización.

Los datos utilizados actualmente son simulados y no contienen información real de usuarios.

## Tecnologías

- Python 3
- CSV y Markdown
- Pandas#
- Docker y Docker Compose
- Git y GitHub
- Visual Studio Code

## Estructura principal

```text
CursoIA/
├── Clase 1/
│   └── proyecto_resuelve_ia.md
├── Clase 2/
│   ├── analisis_de_datos.py
│   ├── informe_proyecto.md
│   └── investigacion_proyectos.md
├── Clase 3/
│   ├── analizar_cultivos.py
│   ├── cultivos.csv
│   ├── informe_cultivos.md
│   ├── datos.txt
│   ├── cultivos.json
│   └── ejercicios de lectura, escritura y excepciones
├── src/
│   ├── analisis_pqrs.py
│   ├── analisis_proyecto.py
│   ├── cargar_datos.py
│   ├── gestion_pqrs.py
│   └── main.py
├── proyectos/
│   └── resuelve-pqrs/          # proyecto de IA aplicado a Resuelve
│       ├── src/                # análisis, preparación ML y neuronas lógicas
│       ├── data/               # datasets propios del proyecto (separados de data/)
│       └── README.md           # problemática y alcance del proyecto
├── Dockerfile
├── docker-compose.yml
└── requirements.txt
```
## Análisis Exploratorio de Datos

Para la Clase 4 se realizó un Análisis Exploratorio de Datos (EDA) sobre el archivo `data/pqrs/pqrs.csv`, utilizando NumPy y Matplotlib.

### Variables analizadas

Se seleccionaron dos variables numéricas relacionadas con la gestión de PQRS:

- `dias_abierta`: cantidad de días que una PQRS permanece abierta.
- `cantidad_adjuntos`: cantidad de archivos adjuntos asociados a cada PQRS.

### Estadísticas descriptivas

Para la variable `dias_abierta` se obtuvieron los siguientes resultados:

- Media: 8.60 días.
- Mediana: 8.00 días.
- Desviación estándar: 4.41 días.
- Mínimo: 3 días.
- Máximo: 15 días.

Para la variable `cantidad_adjuntos`:

- Media: 2.00 adjuntos.
- Mediana: 2.00 adjuntos.
- Desviación estándar: 1.41.
- Mínimo: 0 adjuntos.
- Máximo: 4 adjuntos.

### Visualizaciones

El análisis genera dos gráficos:

![Histograma de días abiertos](data/eda/histograma_dias_abierta.png)

- `data/eda/histograma_dias_abierta.png`: muestra la distribución del tiempo que permanecen abiertas las PQRS.

![Relación entre adjuntos y días abiertos](data/eda/dias_vs_adjuntos.png)
- `data/eda/dias_vs_adjuntos.png`: muestra la relación entre la cantidad de adjuntos y los días que permanece abierta cada PQRS.

### Patrones y relaciones encontradas

En el conjunto de datos utilizado se observa que las PQRS con mayor cantidad de archivos adjuntos también presentan una mayor cantidad de días abiertas.

El coeficiente de correlación entre `cantidad_adjuntos` y `dias_abierta` es aproximadamente `0.9943`, lo que representa una relación positiva muy fuerte dentro de este conjunto de datos.

Sin embargo, los datos utilizados son sintéticos y el conjunto contiene únicamente cinco registros. Por esta razón, esta correlación no permite concluir que la cantidad de adjuntos sea la causa de un mayor tiempo de atención. El resultado debe considerarse como un patrón inicial que podría verificarse posteriormente utilizando un conjunto de datos más amplio.

### Relación con el futuro modelo de Inteligencia Artificial

El análisis exploratorio permite identificar variables que podrían ser útiles para un futuro modelo de Inteligencia Artificial orientado a la gestión y priorización de PQRS.

Variables como el tiempo de apertura, la cantidad de adjuntos, el tipo de solicitud y el estado podrían utilizarse posteriormente para identificar patrones, clasificar solicitudes o estimar cuáles PQRS pueden requerir mayor atención.

Antes de construir un modelo predictivo será necesario disponer de una mayor cantidad de registros y evaluar otras variables relevantes del proceso de gestión de PQRS.

## Avance 2

El segundo corte se desarrolla en [`proyectos/resuelve-pqrs/`](proyectos/resuelve-pqrs/README.md#avance-2),
separado de los ejercicios de clase y sin modificar Resuelve ERP.

- **Preparación:** se conservan los 12 registros sintéticos originales y se
  documentan etiquetas académicas `prioridad_alta` (0 = media/baja; 1 = alta).
  Pandas verifica estructura, tipos, nulos, duplicados e inconsistencias.
  No fueron necesarias correcciones: antes 12×6 y después 12×8, sin nulos.
  Las clases contienen 8 casos de clase 0 y 4 de clase 1.
- **Visualizaciones:** tres gráficos Seaborn con interpretaciones: histograma
  de días, conteo por tipo y dispersión días–longitud según prioridad.
  Se conservan los gráficos y datasets de etapas anteriores.
- **Perceptrón sigmoide:** dos entradas estandarizadas (`dias_desde_radicacion`
  y `longitud_descripcion`), pérdida logarítmica y descenso del gradiente con
  NumPy, sin Scikit-Learn. Se usan 10000 épocas, tasa 0.1 e inicio en cero.
- **Resultados:** `w1=1.5041201103`, `w2=1.9560568515`, `b=-1.1298185501`;
  pérdida de `0.6931471806` a `0.5270863308`; exactitud de entrenamiento
  **75 % (9/12)**. El conjunto no es linealmente separable y no se ha medido
  generalización sobre datos independientes.
- **Verificación:** 19 pruebas aprobadas en Docker (Python 3.13.16),
  reproducibilidad numérica y de gráficos comprobada en dos ejecuciones.

### Ejecución en Docker

Desde la raíz de **CursoIA**, con Docker iniciado y el servicio único `python`:

```bash
docker compose build
docker compose run --rm -e MPLBACKEND=Agg python python proyectos/resuelve-pqrs/src/preparacion_pqrs.py --segundo-corte
docker compose run --rm -e MPLBACKEND=Agg python python proyectos/resuelve-pqrs/src/preparacion_pqrs.py --visualizaciones-segundo-corte
docker compose run --rm -e MPLBACKEND=Agg python python proyectos/resuelve-pqrs/src/perceptron_proyecto.py
docker compose run --rm -e MPLBACKEND=Agg python python -m unittest discover -s proyectos/resuelve-pqrs/tests -v
```

Los CSV preparados están en `proyectos/resuelve-pqrs/data/`. Los gráficos e
interpretaciones están en
[`informes/segundo_corte/interpretaciones.md`](proyectos/resuelve-pqrs/informes/segundo_corte/interpretaciones.md)
y el análisis del modelo en
[`perceptron/interpretacion.md`](proyectos/resuelve-pqrs/informes/segundo_corte/perceptron/interpretacion.md).
Los comandos regeneran únicamente los archivos de su etapa, no el CSV original.

Los resultados son académicos: muestra pequeña, sintética, desbalanceada y
etiquetas subjetivas. No justifican uso operativo. La publicación en GitHub
queda pendiente de autorización; no se generan PDF ni video en este avance.
