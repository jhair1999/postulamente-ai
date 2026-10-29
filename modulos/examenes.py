import random
from datetime import datetime, timezone

import streamlit as st

from datos.preguntas import PREGUNTAS
from modulos.base_datos import (
    crear_intento,
    finalizar_intento,
    guardar_borrador_intento,
    obtener_intento_activo,
    obtener_semana
)


DURACION_MINUTOS = 10
CANTIDAD_PREGUNTAS = 10


def _seleccionar_preguntas():
    semilla = (
        f"{obtener_semana()}-{st.session_state.nombre}-"
        f"{st.session_state.universidad}"
    )
    generador = random.Random(semilla)
    return generador.sample(
        PREGUNTAS, min(CANTIDAD_PREGUNTAS, len(PREGUNTAS))
    )


def guardar_respuesta(pregunta_id):
    examen = st.session_state.get("examen_semanal")
    if not examen or examen["estado"] != "en_curso":
        return
    clave = f"examen_{examen['id']}_{pregunta_id}"
    respuesta = st.session_state.get(clave)
    examen["respuestas"][pregunta_id] = respuesta
    if not guardar_borrador_intento(
        examen["id"], {pregunta_id: respuesta}
    ):
        st.session_state.examen_tiempo_agotado = True


def finalizar_examen():
    examen = st.session_state.get("examen_semanal")
    if not examen or examen["estado"] == "finalizado":
        return examen
    resultado = finalizar_intento(examen["id"], examen["respuestas"])
    st.session_state.examen_semanal = resultado
    st.session_state.examen_tiempo_agotado = False
    return resultado


def mostrar_resultados():
    examen = st.session_state.examen_semanal
    aciertos = examen.get("correctas") or 0
    total = examen.get("total") or len(examen["preguntas"])
    porcentaje = examen.get("puntaje") or 0

    st.success("¡Examen finalizado y guardado!")
    c1, c2, c3 = st.columns(3)
    c1.metric("Correctas", aciertos)
    c2.metric("Incorrectas o vacías", max(0, total - aciertos))
    c3.metric("Calificación", f"{porcentaje}%")

    st.subheader("📚 Revisión de respuestas")
    for numero, pregunta in enumerate(examen["preguntas"], start=1):
        respuesta = examen["respuestas"].get(pregunta["id"])
        with st.expander(f"Pregunta {numero}: {pregunta['tema']}"):
            st.write(pregunta["pregunta"])
            st.write(f"Tu respuesta: {respuesta or 'Sin responder'}")
            st.write(f"Respuesta correcta: {pregunta['respuesta']}")
            for paso in pregunta["explicacion"]:
                st.write("•", paso)

    if st.button("📝 Preparar otro examen semanal"):
        st.session_state.examen_semanal = None
        st.rerun()


@st.fragment(run_every="1s")
def examen_activo():
    examen = st.session_state.examen_semanal
    if examen["estado"] == "finalizado":
        mostrar_resultados()
        return

    restante = int(
        (examen["fin"] - datetime.now(timezone.utc)).total_seconds()
    )
    if restante <= 0 or st.session_state.get(
        "examen_tiempo_agotado", False
    ):
        finalizar_examen()
        st.rerun()
        return

    minutos, segundos = divmod(restante, 60)
    st.warning(f"⏱️ Tiempo restante: {minutos:02d}:{segundos:02d}")
    total = len(examen["preguntas"])

    for numero, pregunta in enumerate(examen["preguntas"], start=1):
        st.subheader(f"Pregunta {numero} de {total}")
        st.caption(
            f"{pregunta['materia']} · {pregunta['tema']} · "
            f"{pregunta['dificultad']}"
        )
        st.write(pregunta["pregunta"])
        clave = f"examen_{examen['id']}_{pregunta['id']}"
        if (
            clave not in st.session_state
            and pregunta["id"] in examen["respuestas"]
        ):
            st.session_state[clave] = examen["respuestas"][pregunta["id"]]
        st.radio(
            "Selecciona tu respuesta:",
            pregunta["opciones"],
            index=None,
            key=clave,
            on_change=guardar_respuesta,
            args=(pregunta["id"],)
        )
        st.divider()

    if st.button("✅ Entregar examen", type="primary"):
        finalizar_examen()
        st.rerun()


def mostrar_examen_semanal():
    st.header("📝 Examen semanal")
    if "examen_semanal" not in st.session_state:
        st.session_state.examen_semanal = None

    examen = st.session_state.examen_semanal
    if examen is None:
        examen = obtener_intento_activo(
            st.session_state.nombre,
            st.session_state.universidad,
            "Semanal",
            "oficial"
        )
        if examen:
            st.session_state.examen_semanal = examen

    if examen:
        if examen["estado"] == "finalizado":
            mostrar_resultados()
        else:
            st.info("Tu examen está guardado y continúa aunque cierres la aplicación.")
            examen_activo()
        return

    st.info(
        "Esta evaluación usa una selección de materias y registra cada "
        "respuesta para personalizar el refuerzo."
    )
    st.write(f"⏱️ Tiempo disponible: {DURACION_MINUTOS} minutos")
    st.write(f"📋 Preguntas: {CANTIDAD_PREGUNTAS}")

    if st.button("🚀 Comenzar examen", type="primary"):
        intento, _ = crear_intento(
            st.session_state.nombre,
            st.session_state.universidad,
            "Semanal",
            "oficial",
            _seleccionar_preguntas(),
            DURACION_MINUTOS,
            convocatoria=obtener_semana()
        )
        st.session_state.examen_semanal = intento
        st.rerun()
