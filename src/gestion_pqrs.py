pqrs_lista = [
    {"radicado": "PQRS-001", "tipo": "Petición", "dias_abierta": 5},
    {"radicado": "PQRS-002", "tipo": "Reclamo", "dias_abierta": 12},
    {"radicado": "PQRS-003", "tipo": "Queja", "dias_abierta": 8},
    {"radicado": "PQRS-004", "tipo": "Sugerencia", "dias_abierta": 3},
    {"radicado": "PQRS-005", "tipo": "Petición", "dias_abierta": 15}
]


def calcular_tiempo_abierta(pqrs):
    return pqrs["dias_abierta"]


def mostrar_pqrs(lista_pqrs):
    for pqrs in lista_pqrs:
        print(
            f"{pqrs['radicado']} - "
            f"{pqrs['tipo']}: "
            f"{calcular_tiempo_abierta(pqrs)} días abierta"
        )


def pqrs_mayor_tiempo_abierta(lista_pqrs):
    return max(lista_pqrs, key=lambda pqrs: pqrs["dias_abierta"])


mostrar_pqrs(pqrs_lista)

mayor = pqrs_mayor_tiempo_abierta(pqrs_lista)

print(
    f"\nPQRS con mayor tiempo abierta: "
    f"{mayor['radicado']} - {mayor['dias_abierta']} días"
)