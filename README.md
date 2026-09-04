# Curso de Inteligencia Artificial

Repositorio académico para desarrollar las actividades del curso de Inteligencia Artificial y el proyecto **Resuelve**, una propuesta orientada al análisis de Peticiones, Quejas, Reclamos y Sugerencias (PQRS).

## Objetivo del proyecto

Aplicar Python, análisis de datos e Inteligencia Artificial para procesar información de PQRS, identificar patrones y generar resultados que apoyen su gestión y priorización.

Los datos utilizados actualmente son simulados y no contienen información real de usuarios.

## Tecnologías

- Python 3
- CSV y Markdown
- Pandas
- Docker y Docker Compose
- Git y GitHub
- Visual Studio Code

## Estructura principal

```text
CursoIA/
├── data/pqrs/pqrs.csv        # Dataset simulado del proyecto Resuelve
├── src/
│   ├── analisis_pqrs.py      # Análisis de PQRS con Pandas
│   ├── analisis_proyecto.py  # Estadísticas e informe del proyecto
│   ├── cargar_datos.py       # Lectura del dataset CSV
│   ├── gestion_pqrs.py       # Ejercicio de gestión de PQRS
│   └── main.py               # Prueba básica del entorno Python
├── analizar_cultivos.py      # Actividad de análisis de cultivos
├── cultivos.csv              # Datos utilizados en la actividad de clase
├── informe_cultivos.md       # Informe generado por analizar_cultivos.py
├── informe_proyecto.md       # Informe generado por analisis_proyecto.py
├── proyecto_resuelve_ia.md   # Descripción de la propuesta del proyecto
├── investigacion_proyectos.md
├── Dockerfile
├── docker-compose.yml
└── requirements.txt
```

## Actividades implementadas

### Análisis de cultivos

`analizar_cultivos.py` lee `cultivos.csv`, convierte los valores numéricos y calcula:

- Total de hectáreas.
- Total de producción.
- Rendimiento promedio por hectárea.
- Cultivo con mayor producción.
- Cultivo con menor producción.

El resultado se guarda en `informe_cultivos.md`.

### Análisis del proyecto Resuelve

`src/analisis_proyecto.py` lee `data/pqrs/pqrs.csv`, calcula estadísticas sobre las solicitudes y genera `informe_proyecto.md` con los resultados y su interpretación.

También se incluyen ejercicios de lectura de CSV, estructuras de datos y análisis con Pandas.

## Ejecución local

Desde la raíz del repositorio:

```bash
python3 analizar_cultivos.py
python3 src/analisis_proyecto.py
python3 src/analisis_pqrs.py
```

## Ejecución con Docker

Construir e iniciar el contenedor:

```bash
docker compose up -d --build
```

Ejecutar uno de los scripts ubicados en `src`:

```bash
docker compose exec python python src/analisis_proyecto.py
```

Detener el entorno:

```bash
docker compose down
```

## Estado actual

- Actividad de análisis de cultivos: completada.
- Actividad independiente con el dataset de PQRS: completada.
- Informes en Markdown: generados.
- Proyecto Resuelve: en desarrollo durante el curso.
