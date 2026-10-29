
import streamlit as st
from datos.preguntas import PREGUNTAS
from modulos.base_datos import guardar_progreso

def iniciar_progreso():
    if "puntos" not in st.session_state:
        st.session_state.puntos = 0

    if "historial" not in st.session_state:
        st.session_state.historial = {}

    if "errores" not in st.session_state:
        st.session_state.errores = {}


def guardar_avance_actual():
    guardar_progreso(
        st.session_state.nombre,
        st.session_state.universidad,
        st.session_state.puntos,
        st.session_state.historial,
        st.session_state.errores
    )


def _crear_registro(ejercicio):
    return {
        "intentos": 0,
        "resuelta": False,
        "materia": ejercicio["materia"],
        "tema": ejercicio["tema"],
        "dificultad": ejercicio.get(
            "dificultad", ejercicio.get("nivel", "Básico")
        ),
        "pistas_usadas": 0,
        "errores": 0,
        "clasificacion": "sin_evidencia"
    }


def registrar_pista(ejercicio):
    iniciar_progreso()
    pregunta_id = ejercicio["id"]
    historial = st.session_state.historial
    if pregunta_id not in historial:
        historial[pregunta_id] = _crear_registro(ejercicio)
    registro = historial[pregunta_id]
    registro.setdefault("pistas_usadas", 0)
    # Una apertura de la ayuda cuenta una sola vez por ejercicio.
    if registro["pistas_usadas"] == 0:
        registro["pistas_usadas"] = 1
        guardar_avance_actual()

def registrar_respuesta(ejercicio, respuesta):
    iniciar_progreso()

    pregunta_id = ejercicio["id"]
    correcta = respuesta == ejercicio["respuesta"]

    historial = st.session_state.historial
    errores = st.session_state.errores

    if pregunta_id not in historial:
        historial[pregunta_id] = _crear_registro(ejercicio)

    registro = historial[pregunta_id]
    registro.setdefault("pistas_usadas", 0)
    registro.setdefault("errores", 0)
    registro.setdefault(
        "dificultad",
        ejercicio.get("dificultad", ejercicio.get("nivel", "Básico"))
    )

    if registro["resuelta"]:
        return correcta, 0, "Esta pregunta ya fue completada."

    registro["intentos"] += 1

    if correcta:
        puntos = 10 if registro["intentos"] == 1 else 5
        registro["resuelta"] = True
        if registro["pistas_usadas"]:
            registro["clasificacion"] = "dominio_con_pista"
        elif registro["intentos"] == 1:
            registro["clasificacion"] = "dominio"
        else:
            registro["clasificacion"] = "procedimiento_en_desarrollo"
        st.session_state.puntos += puntos
        guardar_avance_actual()
        return correcta, puntos, "¡Ejercicio superado!"

    tema = ejercicio["tema"]
    registro["errores"] += 1
    registro["clasificacion"] = (
        "desconoce_tema"
        if registro["errores"] >= 2
        else "error_procedimiento"
    )
    errores[tema] = errores.get(tema, 0) + 1
    guardar_avance_actual()
    return correcta, 0, "Revisa la explicación e inténtalo nuevamente."


def obtener_estadisticas():
    iniciar_progreso()

    historial = st.session_state.historial
    total = len(PREGUNTAS)

    completadas = sum(
        1 for r in historial.values() if r["resuelta"]
    )

    porcentaje = (
        round(completadas / total * 100)
        if total > 0 else 0
    )

    puntos = st.session_state.puntos

    if puntos < 50:
        nivel = "Principiante"
    elif puntos < 150:
        nivel = "Intermedio"
    else:
        nivel = "Avanzado"

    return puntos, nivel, porcentaje
