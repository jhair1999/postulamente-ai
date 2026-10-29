from collections import defaultdict

import streamlit as st

from datos.preguntas import PREGUNTAS
from modulos.base_datos import obtener_resumen_respuestas
from modulos.refuerzo import mostrar_refuerzo


PRERREQUISITOS = defaultdict(list)
for _pregunta in PREGUNTAS:
    for _requisito in _pregunta.get("prerrequisitos", []):
        if (
            _requisito != _pregunta["tema"]
            and _requisito not in PRERREQUISITOS[_pregunta["tema"]]
        ):
            PRERREQUISITOS[_pregunta["tema"]].append(_requisito)


def _evidencia_practicas():
    evidencia = defaultdict(
        lambda: {
            "total": 0,
            "correctas": 0,
            "errores": 0,
            "con_pista": 0
        }
    )
    historial = st.session_state.get("historial", {})
    for registro in historial.values():
        tema = registro.get("tema")
        if not tema:
            continue
        datos = evidencia[tema]
        errores = int(registro.get("errores", 0))
        correcta = int(bool(registro.get("resuelta", False)))
        datos["errores"] += errores
        datos["correctas"] += correcta
        datos["total"] += errores + correcta
        if correcta and registro.get("pistas_usadas", 0):
            datos["con_pista"] += 1

    # Compatibilidad con progresos guardados antes del diagnóstico detallado.
    for tema, cantidad in st.session_state.get("errores", {}).items():
        datos = evidencia[tema]
        diferencia = max(0, int(cantidad) - datos["errores"])
        datos["errores"] += diferencia
        datos["total"] += diferencia
    return evidencia


def _clasificar(datos):
    correctas = datos["correctas"]
    errores = datos["errores"]
    con_pista = datos["con_pista"]
    if errores >= 2 and correctas == 0:
        return (
            "No conoce aún el tema",
            "Básico",
            "Conviene reconstruir los conceptos y practicar con ejemplos guiados."
        )
    if errores > 0 and correctas > 0:
        return (
            "Comete errores de procedimiento",
            "Básico o intermedio",
            "Comprende parte del tema, pero debe revisar los pasos donde falla."
        )
    if con_pista > 0:
        return (
            "Resuelve correctamente con pistas",
            "Intermedio",
            "Debe repetir ejercicios similares reduciendo gradualmente la ayuda."
        )
    if correctas > 0 and errores == 0:
        return (
            "Demuestra dominio sin ayuda",
            "Intermedio o avanzado",
            "Puede avanzar a problemas más difíciles y de transferencia."
        )
    return (
        "Evidencia insuficiente",
        "Básico",
        "Necesita resolver más actividades para obtener un diagnóstico confiable."
    )


def analizar_estudiante():
    combinada = _evidencia_practicas()
    for registro in obtener_resumen_respuestas(
        st.session_state.nombre,
        st.session_state.universidad
    ):
        datos = combinada[registro["tema"]]
        for campo in ("total", "correctas", "errores", "con_pista"):
            datos[campo] += registro[campo]

    if not combinada:
        return {
            "estado": "sin_datos",
            "mensaje": "Comienza resolviendo ejercicios o un examen.",
            "tema": None,
            "recomendaciones": [],
            "diagnosticos": []
        }

    diagnosticos = []
    for tema, datos in combinada.items():
        diagnostico, dificultad, accion = _clasificar(datos)
        diagnosticos.append({
            "tema": tema,
            **datos,
            "diagnostico": diagnostico,
            "dificultad": dificultad,
            "accion": accion,
            "prioridad": datos["errores"] * 2 + datos["con_pista"]
                         - datos["correctas"] * 0.5
        })

    diagnosticos.sort(
        key=lambda item: (item["prioridad"], item["errores"]),
        reverse=True
    )
    principal = diagnosticos[0]
    necesita_refuerzo = principal["errores"] > 0 or principal["con_pista"] > 0
    recomendaciones = PRERREQUISITOS.get(
        principal["tema"], ["Repasar la teoría", "Resolver ejemplos guiados"]
    )

    return {
        "estado": "refuerzo" if necesita_refuerzo else "progreso",
        "mensaje": (
            f"Prioridad actual: {principal['tema']}. "
            f"{principal['diagnostico']}."
            if necesita_refuerzo
            else "La evidencia registrada muestra un buen avance."
        ),
        "tema": principal["tema"],
        "recomendaciones": recomendaciones,
        "diagnosticos": diagnosticos,
        "dificultad": principal["dificultad"],
        "accion": principal["accion"]
    }


def mostrar_agente():
    st.header("🤖 Tutor inteligente")
    st.write(
        "El tutor combina prácticas, exámenes y simulacros guardados para "
        "mantener un modelo transparente de tu aprendizaje."
    )
    resultado = analizar_estudiante()

    if resultado["estado"] == "sin_datos":
        st.info(resultado["mensaje"])
        return
    if resultado["estado"] == "progreso":
        st.success(resultado["mensaje"])
    else:
        st.warning(resultado["mensaje"])

    c1, c2 = st.columns(2)
    c1.metric("Tema priorizado", resultado["tema"])
    c2.metric("Dificultad recomendada", resultado["dificultad"])
    st.info(f"🤖 Acción educativa: {resultado['accion']}")

    with st.expander("🔎 Ver evidencias utilizadas"):
        for item in resultado["diagnosticos"]:
            st.write(
                f"**{item['tema']}** — {item['diagnostico']} · "
                f"{item['correctas']} correctas, {item['errores']} errores, "
                f"{item['con_pista']} con pista"
            )

    if resultado["estado"] != "refuerzo":
        return

    st.subheader("📚 Plan de refuerzo recomendado")
    for i, tema in enumerate(resultado["recomendaciones"], start=1):
        st.write(f"{i}. {tema}")

    st.divider()
    tema_seleccionado = st.selectbox(
        "¿Qué concepto quieres aprender?",
        resultado["recomendaciones"]
    )
    if st.toggle("🎓 Iniciar clase personalizada"):
        mostrar_refuerzo(tema_seleccionado)
