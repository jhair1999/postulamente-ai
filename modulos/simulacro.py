from datetime import datetime, timezone

import streamlit as st

from datos.preguntas import PREGUNTAS
from modulos.base_datos import (
    crear_intento,
    finalizar_intento,
    guardar_borrador_intento,
    obtener_intento_activo,
    obtener_mes,
    obtener_simulacro_oficial
)


DURACION_MINUTOS = 15


def _guardar_respuesta(pregunta_id):
    simulacro = st.session_state.get("simulacro")
    if not simulacro or simulacro["estado"] != "en_curso":
        return
    clave = f"simulacro_{simulacro['id']}_{pregunta_id}"
    respuesta = st.session_state.get(clave)
    simulacro["respuestas"][pregunta_id] = respuesta
    if not guardar_borrador_intento(
        simulacro["id"], {pregunta_id: respuesta}
    ):
        st.session_state.simulacro_tiempo_agotado = True


def finalizar_simulacro():
    simulacro = st.session_state.get("simulacro")
    if not simulacro or simulacro["estado"] == "finalizado":
        return simulacro
    resultado = finalizar_intento(
        simulacro["id"], simulacro["respuestas"]
    )
    st.session_state.simulacro = resultado
    st.session_state.simulacro_tiempo_agotado = False
    return resultado


def _mostrar_resultados(simulacro):
    etiqueta = (
        "oficial para el ranking"
        if simulacro["modalidad"] == "oficial"
        else "de práctica"
    )
    st.success(f"Simulacro {etiqueta} finalizado")
    c1, c2, c3 = st.columns(3)
    c1.metric("Puntaje", f"{simulacro.get('puntaje') or 0}%")
    c2.metric("Correctas", simulacro.get("correctas") or 0)
    c3.metric("Total", simulacro.get("total") or 0)

    if simulacro["modalidad"] == "oficial":
        st.info(
            "Este es tu único resultado oficial de la convocatoria "
            f"{simulacro.get('convocatoria') or obtener_mes()}."
        )
    else:
        st.caption("La práctica no modifica el ranking mensual.")

    if simulacro["preguntas"]:
        st.subheader("📚 Revisión de respuestas")
        for numero, pregunta in enumerate(simulacro["preguntas"], start=1):
            respuesta = simulacro["respuestas"].get(pregunta["id"])
            with st.expander(f"Pregunta {numero}: {pregunta['tema']}"):
                st.write(pregunta["pregunta"])
                st.write(f"Tu respuesta: {respuesta or 'Sin responder'}")
                st.write(f"Respuesta correcta: {pregunta['respuesta']}")
                for paso in pregunta["explicacion"]:
                    st.write("•", paso)

    if simulacro["modalidad"] == "practica":
        if st.button("🔄 Iniciar otra práctica"):
            st.session_state.simulacro = None
            st.rerun()


@st.fragment(run_every="1s")
def _simulacro_activo():
    simulacro = st.session_state.simulacro
    if simulacro["estado"] == "finalizado":
        _mostrar_resultados(simulacro)
        return

    restante = int(
        (simulacro["fin"] - datetime.now(timezone.utc)).total_seconds()
    )
    if restante <= 0 or st.session_state.get(
        "simulacro_tiempo_agotado", False
    ):
        finalizar_simulacro()
        st.rerun()
        return

    minutos, segundos = divmod(restante, 60)
    st.warning(f"⏱️ Tiempo restante: {minutos:02d}:{segundos:02d}")
    st.progress(
        min(1.0, max(0.0, restante / (DURACION_MINUTOS * 60)))
    )

    total = len(simulacro["preguntas"])
    for numero, pregunta in enumerate(simulacro["preguntas"], start=1):
        st.subheader(f"Pregunta {numero} de {total}")
        st.caption(
            f"{pregunta['materia']} · {pregunta['tema']} · "
            f"{pregunta['dificultad']}"
        )
        st.write(pregunta["pregunta"])
        clave = f"simulacro_{simulacro['id']}_{pregunta['id']}"
        if (
            clave not in st.session_state
            and pregunta["id"] in simulacro["respuestas"]
        ):
            st.session_state[clave] = simulacro["respuestas"][pregunta["id"]]
        st.radio(
            "Selecciona tu respuesta:",
            pregunta["opciones"],
            index=None,
            key=clave,
            on_change=_guardar_respuesta,
            args=(pregunta["id"],)
        )
        st.divider()

    if st.button("✅ Finalizar simulacro", type="primary"):
        finalizar_simulacro()
        st.rerun()


def _recuperar_intento(modalidad):
    estudiante = st.session_state.nombre
    universidad = st.session_state.universidad
    if modalidad == "oficial":
        return obtener_simulacro_oficial(estudiante, universidad)
    return obtener_intento_activo(
        estudiante, universidad, "Mensual", "practica"
    )


def mostrar_simulacro():
    st.header("🏆 Simulacro mensual")
    st.write(
        "Practica libremente o registra un único intento oficial "
        "para el ranking de tu universidad."
    )

    if "simulacro" not in st.session_state:
        st.session_state.simulacro = None

    activo = st.session_state.simulacro
    if activo is None:
        oficial_pendiente = obtener_simulacro_oficial(
            st.session_state.nombre,
            st.session_state.universidad
        )
        if oficial_pendiente and oficial_pendiente["estado"] == "en_curso":
            activo = oficial_pendiente
            st.session_state.simulacro = activo

    modalidad_bloqueada = bool(activo and activo["estado"] == "en_curso")
    modalidad_inicial = (
        activo["modalidad"] if activo else "practica"
    )
    etiquetas = {"Práctica": "practica", "Oficial": "oficial"}
    inversa = {valor: clave for clave, valor in etiquetas.items()}
    seleccion = st.radio(
        "Modalidad",
        list(etiquetas),
        index=list(etiquetas).index(inversa[modalidad_inicial]),
        horizontal=True,
        disabled=modalidad_bloqueada,
        help=(
            "El intento oficial participa en el ranking y solo puede "
            "realizarse una vez por convocatoria."
        )
    )
    modalidad = activo["modalidad"] if modalidad_bloqueada else etiquetas[seleccion]

    if activo and activo["modalidad"] != modalidad and activo["estado"] == "finalizado":
        st.session_state.simulacro = None
        activo = None

    if activo is None:
        activo = _recuperar_intento(modalidad)
        if activo:
            st.session_state.simulacro = activo

    if activo:
        if activo["estado"] == "finalizado":
            _mostrar_resultados(activo)
        else:
            if activo["inicio"] < datetime.now(timezone.utc):
                st.info("Se recuperó tu intento pendiente desde la base de datos.")
            _simulacro_activo()
        return

    st.write(f"⏱️ Duración: {DURACION_MINUTOS} minutos")
    st.write(f"📋 Preguntas: {len(PREGUNTAS)}")
    if modalidad == "oficial":
        st.warning(
            "Al iniciarlo, este será tu intento oficial de la convocatoria "
            f"{obtener_mes()}. Si cierras la aplicación, el tiempo continúa."
        )
        texto_boton = "🚀 Iniciar intento oficial"
    else:
        st.info("Puedes repetir esta modalidad y no afectará el ranking.")
        texto_boton = "🎯 Iniciar práctica"

    if st.button(texto_boton, type="primary"):
        intento, creado = crear_intento(
            st.session_state.nombre,
            st.session_state.universidad,
            "Mensual",
            modalidad,
            PREGUNTAS,
            DURACION_MINUTOS,
            convocatoria=obtener_mes() if modalidad == "oficial" else None
        )
        st.session_state.simulacro = intento
        if not creado and modalidad == "oficial":
            st.info("Ya existe tu intento oficial de esta convocatoria.")
        st.rerun()
