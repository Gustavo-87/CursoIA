import csv


def leer_cultivos(archivo_csv):
    cultivos = []

    with open(archivo_csv, "r", encoding="utf-8") as archivo:
        lector = csv.DictReader(archivo)

        for fila in lector:
            cultivo = {
                "nombre": fila["nombre"],
                "hectareas": float(fila["hectareas"]),
                "produccion_toneladas": float(
                    fila["produccion_toneladas"]
                ),
            }
            cultivos.append(cultivo)

    return cultivos


def calcular_estadisticas(cultivos):
    total_hectareas = sum(cultivo["hectareas"] for cultivo in cultivos)
    total_produccion = sum(
        cultivo["produccion_toneladas"] for cultivo in cultivos
    )

    promedio_rendimiento = (
        total_produccion / total_hectareas
        if total_hectareas > 0
        else 0
    )

    mayor = max(
        cultivos,
        key=lambda cultivo: cultivo["produccion_toneladas"],
    )
    menor = min(
        cultivos,
        key=lambda cultivo: cultivo["produccion_toneladas"],
    )

    return {
        "total_hectareas": total_hectareas,
        "total_produccion": total_produccion,
        "promedio_rendimiento": promedio_rendimiento,
        "cultivo_mayor_produccion": mayor["nombre"],
        "cultivo_menor_produccion": menor["nombre"],
    }


def generar_informe(estadisticas, archivo_salida):
    with open(archivo_salida, "w", encoding="utf-8") as archivo:
        archivo.write("# Informe de Cultivos\n\n")
        archivo.write(
            f"**Total de hectáreas:** "
            f"{estadisticas['total_hectareas']:.2f}\n\n"
        )
        archivo.write(
            f"**Total de producción:** "
            f"{estadisticas['total_produccion']:.2f} toneladas\n\n"
        )
        archivo.write(
            f"**Promedio de rendimiento:** "
            f"{estadisticas['promedio_rendimiento']:.2f} ton/ha\n\n"
        )
        archivo.write(
            f"**Cultivo con mayor producción:** "
            f"{estadisticas['cultivo_mayor_produccion']}\n\n"
        )
        archivo.write(
            f"**Cultivo con menor producción:** "
            f"{estadisticas['cultivo_menor_produccion']}\n"
        )


if __name__ == "__main__":
    cultivos = leer_cultivos("cultivos.csv")
    estadisticas = calcular_estadisticas(cultivos)
    generar_informe(estadisticas, "informe_cultivos.md")

    print("Informe generado correctamente: informe_cultivos.md")