
from modulos.base_datos import (
    obtener_examenes_semanales,
    obtener_historial_mensual
)


def calcular_dominio(estudiante, universidad):
    semanales = obtener_examenes_semanales(
        estudiante, universidad
    )

    mensuales = obtener_historial_mensual(
        estudiante, universidad
    )

    if not semanales and not mensuales:
        return {
            "porcentaje": None,
            "nivel": "Sin evaluación",
            "recomendacion": "Realiza tu primer examen."
        }

    valores = []
    pesos = []

    if semanales:
        # Consideramos hasta los 4 exámenes más recientes.
        ultimos = semanales[:4]
        promedio = sum(
            examen[1] for examen in ultimos
        ) / len(ultimos)

        valores.append(promedio)
        pesos.append(0.40)

    if mensuales:
        # Último simulacro mensual.
        valores.append(mensuales[0][1])
        pesos.append(0.60)

    porcentaje = round(
        sum(v * p for v, p in zip(valores, pesos))
        / sum(pesos)
    )

    if porcentaje < 40:
        nivel = "Necesita refuerzo"
        recomendacion = (
            "Refuerza los conceptos básicos "
            "antes de avanzar."
        )
    elif porcentaje < 70:
        nivel = "En desarrollo"
        recomendacion = (
            "Continúa practicando y revisa "
            "los ejercicios incorrectos."
        )
    elif porcentaje < 90:
        nivel = "Buen rendimiento"
        recomendacion = (
            "Practica ejercicios de mayor dificultad."
        )
    else:
        nivel = "Rendimiento destacado"
        recomendacion = (
            "Mantén tu preparación con "
            "simulacros y problemas avanzados."
        )

    return {
        "porcentaje": porcentaje,
        "nivel": nivel,
        "recomendacion": recomendacion
    }
