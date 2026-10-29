
import streamlit as st
from datos.preguntas import PREGUNTAS
from modulos.progreso import (
    iniciar_progreso,
    registrar_respuesta,
    registrar_pista,
    obtener_estadisticas
)


def mostrar_juegos():
    iniciar_progreso()

    st.header("🎮 Practicar jugando")
    st.write(
        "Supera retos matemáticos, consigue puntos "
        "y avanza en tu preparación universitaria."
    )

    puntos, nivel, _ = obtener_estadisticas()

    c1, c2, c3 = st.columns(3)
    c1.metric("⭐ Puntos", puntos)
    c2.metric("🏅 Nivel", nivel)
    c3.metric(
        "🎯 Ejercicios completados",
        sum(
            1 for r in st.session_state.historial.values()
            if r["resuelta"]
        )
    )

    st.divider()

    # Selección de materia
    materias = sorted(set(
        p["materia"] for p in PREGUNTAS
    ))

    materia = st.selectbox(
        "📚 Selecciona tu materia",
        materias,
        key="juego_materia"
    )

    historial = st.session_state.historial

    pendientes = [
        p for p in PREGUNTAS
        if p["materia"] == materia
        and not historial.get(
            p["id"], {}
        ).get("resuelta", False)
    ]

    registros_materia = [
        registro for registro in historial.values()
        if registro.get("materia") == materia
    ]
    if any(
        registro.get("clasificacion") == "desconoce_tema"
        for registro in registros_materia
    ):
        dificultad_objetivo = "Básico"
    elif sum(
        registro.get("clasificacion") == "dominio"
        for registro in registros_materia
    ) >= 2:
        dificultad_objetivo = "Intermedio"
    else:
        dificultad_objetivo = "Básico"

    orden_dificultad = {"Básico": 0, "Intermedio": 1, "Avanzado": 2}
    pendientes.sort(
        key=lambda pregunta: abs(
            orden_dificultad.get(pregunta["dificultad"], 0)
            - orden_dificultad[dificultad_objetivo]
        )
    )

    st.subheader("🏆 Desafío matemático")

    if not pendientes:
        st.success(
            "¡Completaste todos los retos disponibles "
            "de esta materia!"
        )

        st.info(
            "Pronto se agregarán más preguntas."
        )
        return

    # Elegimos el primer reto pendiente.
    # Así no cambia la pregunta en cada actualización.
    ejercicio = pendientes[0]

    st.info(
        "🤖 Selección adaptativa: el tutor recomienda dificultad "
        f"**{dificultad_objetivo}** según tu progreso guardado."
    )

    st.write(f"**Tema:** {ejercicio['tema']}")
    st.write(f"**Dificultad:** {ejercicio['nivel']}")

    st.progress(
        1 - len(pendientes) /
        max(
            1,
            len([
                p for p in PREGUNTAS
                if p["materia"] == materia
            ])
        )
    )

    st.markdown(f"### {ejercicio['pregunta']}")

    respuesta = st.radio(
        "Elige tu respuesta:",
        ejercicio["opciones"],
        index=None,
        key=f"juego_respuesta_{ejercicio['id']}"
    )

    if st.button(
        "✅ Comprobar",
        key=f"juego_comprobar_{ejercicio['id']}"
    ):
        if respuesta is None:
            st.warning("Selecciona una respuesta.")
        else:
            correcta, ganados, mensaje = registrar_respuesta(
                ejercicio, respuesta
            )

            if correcta:
                st.balloons()
                st.success(
                    f"🎉 ¡Reto superado! +{ganados} puntos"
                )
                st.info(
                    "Presiona 'Siguiente reto' "
                    "para continuar."
                )
            else:
                st.error(
                    "Respuesta incorrecta. "
                    "Revisa la explicación e inténtalo."
                )

    if st.toggle(
        "💡 Necesito una pista",
        key=f"juego_pista_{ejercicio['id']}"
    ):
        registrar_pista(ejercicio)
        for pista in ejercicio.get(
            "pistas", ["Revisa qué operación necesitas."]
        ):
            st.write("•", pista)

    with st.expander("📖 Explicación paso a paso"):
        for i, paso in enumerate(
            ejercicio["explicacion"], 1
        ):
            st.write(f"**Paso {i}:** {paso}")

    if historial.get(
        ejercicio["id"], {}
    ).get("resuelta", False):
        if st.button("➡️ Siguiente reto"):
            st.rerun()
