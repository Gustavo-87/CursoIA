# Curso de Inteligencia Artificial — Clasificación de PQRS

Proyecto académico de clasificación de prioridad de Peticiones, Quejas, Reclamos y Sugerencias (PQRS) mediante Python, NumPy y Scikit-Learn. Se utilizan **150 registros sintéticos** para entrenar y comparar modelos.

## Paso a paso para instalar y ejecutar el proyecto

**Sigue los pasos en orden.** Ejecuta cada comando en una terminal y comprueba su resultado antes de continuar. El proyecto funciona mediante scripts de Python dentro de Docker; **no requiere abrir una página web**.

### Paso 1. Instalar los programas necesarios

El computador debe contar con:

- [Git](https://git-scm.com/downloads).
- [Docker Desktop](https://www.docker.com/products/docker-desktop/) (Windows o macOS), o Docker Engine con Compose (Linux).
- Conexión a Internet para la descarga inicial.

Abre **Docker Desktop** y comprueba en una terminal que los programas estén disponibles:

```bash
git --version
docker --version
docker compose version
```

Comprueba que el motor de Docker esté funcionando:

```bash
docker info
```

**Resultado esperado:** los comandos muestran información de las versiones y del motor Docker, sin errores de conexión. Si `docker info` falla, inicia Docker Desktop y repite la comprobación.

**No es necesario instalar Python ni bibliotecas de Python en el computador.**

### Paso 2. Descargar el repositorio

En una terminal, ubícate en la carpeta donde desees guardar el proyecto y ejecuta:

```bash
git clone https://github.com/Gustavo-87/CursoIA.git
```

Después, ingresa a la carpeta descargada:

```bash
cd CursoIA
```

**Resultado esperado:** la terminal queda ubicada dentro de `CursoIA`.

**Importante:** todos los comandos restantes se ejecutan **desde la raíz de `CursoIA`**, donde se encuentra el `docker-compose.yml` principal. No ingreses a `proyectos/resuelve-pqrs/` para ejecutar estos comandos.

### Paso 3. Verificar la configuración de Docker Compose

Ejecuta:

```bash
docker compose config --services
```

**Resultado esperado:**

```text
python
```

Si aparece `python_ia` o no aparece `python`, comprueba que la terminal esté en la raíz de `CursoIA` y no en la carpeta del subproyecto.

### Paso 4. Construir el entorno de ejecución

Ejecuta:

```bash
docker compose build
```

**Resultado esperado:** Docker construye la imagen e instala las bibliotecas definidas en `requirements.txt` sin errores. La primera construcción requiere descargar la imagen de Python 3.13 y sus dependencias.

Comprueba que Python funciona dentro del contenedor:

```bash
docker compose run --rm python python --version
```

**Resultado esperado:** se muestra `Python 3.13.x`.

El comando `docker compose run --rm` ejecuta cada programa en un contenedor temporal. No es necesario ejecutar `docker compose up`.

### Paso 5. Preparar los datos del segundo corte

Ejecuta:

```bash
docker compose run --rm -e MPLBACKEND=Agg python python proyectos/resuelve-pqrs/src/preparacion_pqrs.py --segundo-corte
```

**Resultado esperado:** el programa analiza **12 registros sintéticos**, valida su calidad y genera estos archivos:

- `proyectos/resuelve-pqrs/data/pqrs_limpias_segundo_corte.csv`
- `proyectos/resuelve-pqrs/data/pqrs_ml_segundo_corte.csv`
- `proyectos/resuelve-pqrs/data/resumen_limpieza_segundo_corte.csv`

### Paso 6. Generar los gráficos del segundo corte

Ejecuta:

```bash
docker compose run --rm -e MPLBACKEND=Agg python python proyectos/resuelve-pqrs/src/preparacion_pqrs.py --visualizaciones-segundo-corte
```

**Resultado esperado:** se generan tres gráficos y el archivo `interpretaciones.md` dentro de `proyectos/resuelve-pqrs/informes/segundo_corte/`.

### Paso 7. Entrenar el perceptrón del segundo corte

Ejecuta:

```bash
docker compose run --rm -e MPLBACKEND=Agg python python proyectos/resuelve-pqrs/src/perceptron_proyecto.py
```

**Resultado esperado:** la terminal muestra los pesos, el sesgo, la pérdida y la exactitud de entrenamiento sobre los 12 casos. Como referencia, la exactitud documentada es **9/12 (75 %)**. Se generan la curva de aprendizaje y la frontera de decisión en `proyectos/resuelve-pqrs/informes/segundo_corte/perceptron/`.

### Paso 8. Generar el conjunto de datos final

Ejecuta:

```bash
docker compose run --rm -e MPLBACKEND=Agg python python proyectos/resuelve-pqrs/src/generar_datos.py
```

**Resultado esperado:** se crea o regenera `proyectos/resuelve-pqrs/data/pqrs_final_150.csv`, con **150 registros sintéticos**: 120 de prioridad no alta (0) y 30 de prioridad alta (1). El script utiliza la semilla 42.

### Paso 9. Entrenar el perceptrón final con NumPy

Ejecuta:

```bash
docker compose run --rm -e MPLBACKEND=Agg python python proyectos/resuelve-pqrs/src/perceptron_final.py
```

**Resultado esperado:** se muestran las métricas de entrenamiento y prueba del perceptrón, y se genera `proyectos/resuelve-pqrs/graficos_final/curva_perceptron.png`.

### Paso 10. Entrenar y comparar los modelos de clasificación

Ejecuta:

```bash
docker compose run --rm -e MPLBACKEND=Agg python python proyectos/resuelve-pqrs/src/modelo_proyecto.py
```

**Resultado esperado:** la terminal presenta la comparación de **regresión logística, KNN y árbol de decisión**, con exactitud, precisión, recall y F1. El modelo se selecciona según el F1 promedio de validación cruzada de cinco pliegues.

Además, se generan:

- `proyectos/resuelve-pqrs/modelo_pqrs_final.joblib` — modelo seleccionado.
- `proyectos/resuelve-pqrs/graficos_final/matriz_confusion.png`
- `proyectos/resuelve-pqrs/graficos_final/real_vs_predicho.png`

**Valores de referencia documentados:** regresión logística como modelo seleccionado, F1 de validación cruzada cercano a 0.433 y exactitud de prueba cercana a 0.767. Las versiones actuales de las bibliotecas no están fijadas en `requirements.txt`, por lo que los resultados pueden variar entre instalaciones.

### Paso 11. Realizar predicciones con el modelo guardado

Ejecuta este comando **después del paso 10**:

```bash
docker compose run --rm -e MPLBACKEND=Agg python python proyectos/resuelve-pqrs/src/usar_modelo.py
```

**Resultado esperado:** el programa carga `modelo_pqrs_final.joblib` y muestra las predicciones de tres PQRS nuevas, sin volver a entrenar. Con el modelo documentado, sus clasificaciones son **No alta**, **No alta** y **Alta**.

### Paso 12. Ejecutar las pruebas automatizadas

Ejecuta:

```bash
docker compose run --rm -e MPLBACKEND=Agg python python -m unittest discover -s proyectos/resuelve-pqrs/tests -v
```

**Resultado esperado:** se ejecutan las **19 pruebas automatizadas del segundo corte** y, si todas pasan, la salida termina con `OK`.

Estas pruebas cubren la preparación de datos, las visualizaciones y el perceptrón del segundo corte. Los pasos 8 a 11 permiten verificar por separado el flujo del modelo final.

### Paso 13. Revisar los resultados y el informe

Los archivos generados quedan en el repositorio local, en las rutas indicadas en cada paso.

- [Código y documentación del proyecto de PQRS](proyectos/resuelve-pqrs/README.md)
- [Carpeta de gráficos finales](proyectos/resuelve-pqrs/graficos_final/)
- [Carpeta de informes del segundo corte](proyectos/resuelve-pqrs/informes/segundo_corte/)
- [Informe final en PDF](proyectos/resuelve-pqrs/docs/Informe_Final_Integraci%C3%B3n%20de%20IA%20para%20la%20Gesti%C3%B3n%20de%20PQRS.pdf)

### Paso 14. Finalizar

No es necesario detener contenedores manualmente: `run --rm` elimina cada contenedor al finalizar. Para limpiar recursos de Docker Compose de manera opcional:

```bash
docker compose down
```

Para ejecutar nuevamente el proyecto, conserva la carpeta `CursoIA` y repite los pasos **5 a 12**. No es necesario clonar ni construir otra vez, salvo que cambien las dependencias o el Dockerfile.

## Alcance

Los datos de PQRS son **sintéticos**. En el conjunto final, la etiqueta de prioridad se obtiene mediante una regla basada en las mismas variables predictoras; por ello, las métricas no demuestran validez predictiva sobre solicitudes reales. El desarrollo es académico y no está integrado en producción con Resuelve ERP.

## Otros materiales del curso

Las actividades de clases anteriores permanecen en las carpetas `Clase 1/`, `Clase 2/`, `Clase 3/`, `src/` y `data/`. El historial de preparación, perceptrón y modelos de PQRS se documenta en el [README del subproyecto](proyectos/resuelve-pqrs/README.md).
