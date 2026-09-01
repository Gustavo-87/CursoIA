import csv


def leer_datos(ruta_archivo):
    """Lee el archivo CSV de PQRS y retorna una lista de diccionarios."""
    datos = []

    with open(ruta_archivo, "r", encoding="utf-8") as archivo:
        lector = csv.DictReader(archivo)

        for fila in lector:
            fila["dias_abierta"] = int(fila["dias_abierta"])
            datos.append(fila)

    return datos


def calcular_estadisticas(datos):
    """Calcula estadísticas relevantes de las PQRS."""
    total_pqrs = len(datos)

    dias = [pqrs["dias_abierta"] for pqrs in datos]

    promedio_dias = sum(dias) / total_pqrs
    maximo_dias = max(dias)
    minimo_dias = min(dias)

    pqrs_mas_antigua = max(datos, key=lambda pqrs: pqrs["dias_abierta"])

    estados = {}
    tipos = {}

    for pqrs in datos:
        estado = pqrs["estado"]
        tipo = pqrs["tipo"]

        estados[estado] = estados.get(estado, 0) + 1
        tipos[tipo] = tipos.get(tipo, 0) + 1

    return {
        "total_pqrs": total_pqrs,
        "promedio_dias": promedio_dias,
        "maximo_dias": maximo_dias,
        "minimo_dias": minimo_dias,
        "pqrs_mas_antigua": pqrs_mas_antigua,
        "estados": estados,
        "tipos": tipos,
    }


def generar_informe(estadisticas, archivo_salida):
    """Genera un informe Markdown con las estadísticas obtenidas."""

    with open(archivo_salida, "w", encoding="utf-8") as archivo:
        archivo.write("# Informe del Proyecto de Inteligencia Artificial - Resuelve\n\n")

        archivo.write("## Descripción de los datos\n\n")
        archivo.write(
            "El conjunto de datos contiene información simulada de PQRS "
            "registradas en la plataforma Resuelve. Se analizan el tipo de "
            "solicitud, su estado y la cantidad de días que permanece abierta.\n\n"
        )

        archivo.write("## Estadísticas\n\n")
        archivo.write("| Estadística | Resultado |\n")
        archivo.write("|---|---|\n")
        archivo.write(
            f"| Total de PQRS | {estadisticas['total_pqrs']} |\n"
        )
        archivo.write(
            f"| Promedio de días abiertos | {estadisticas['promedio_dias']:.2f} |\n"
        )
        archivo.write(
            f"| Máximo de días abierta | {estadisticas['maximo_dias']} |\n"
        )
        archivo.write(
            f"| Mínimo de días abierta | {estadisticas['minimo_dias']} |\n"
        )
        archivo.write(
            f"| PQRS con mayor tiempo abierta | "
            f"{estadisticas['pqrs_mas_antigua']['radicado']} |\n"
        )

        archivo.write("\n## Cantidad de PQRS por estado\n\n")

        for estado, cantidad in estadisticas["estados"].items():
            archivo.write(f"- {estado}: {cantidad}\n")

        archivo.write("\n## Cantidad de PQRS por tipo\n\n")

        for tipo, cantidad in estadisticas["tipos"].items():
            archivo.write(f"- {tipo}: {cantidad}\n")

        archivo.write("\n## Interpretación de los resultados\n\n")
        archivo.write(
            "Las estadísticas permiten identificar cuánto tiempo permanecen "
            "abiertas las solicitudes y cuáles casos requieren mayor atención. "
            "También permiten observar la distribución de las PQRS por tipo y "
            "estado, información que puede servir como base para identificar "
            "patrones y apoyar la priorización de solicitudes dentro de Resuelve.\n"
        )


if __name__ == "__main__":
    try:
        datos_pqrs = leer_datos("data/pqrs/pqrs.csv")

        if not datos_pqrs:
            print("El archivo no contiene registros para analizar.")
        else:
            estadisticas = calcular_estadisticas(datos_pqrs)
            generar_informe(estadisticas, "informe_proyecto.md")

            print("Análisis completado correctamente.")
            print("Informe generado: informe_proyecto.md")

    except FileNotFoundError:
        print("Error: no se encontró el archivo data/pqrs/pqrs.csv.")

    except ValueError:
        print("Error: se encontró un valor numérico con formato incorrecto.")
