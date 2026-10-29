
import streamlit as st
import pandas as pd

from modulos.base_datos import (
    obtener_ranking,
    obtener_mes
)


def mostrar_ranking():
    st.header("🏆 Ranking mensual de postulantes")

    universidad = st.session_state.universidad
    estudiante = st.session_state.nombre

    st.write(f"🎓 Universidad: **{universidad}**")
    st.write(f"📅 Convocatoria: **{obtener_mes()}**")

    ranking = obtener_ranking(universidad)

    if not ranking:
        st.info(
            "Todavía no hay resultados registrados "
            "para esta convocatoria."
        )
        return

    datos = []

    for posicion, (nombre, puntaje) in enumerate(
        ranking, start=1
    ):
        datos.append({
            "Puesto": posicion,
            "Estudiante": nombre,
            "Puntaje (%)": puntaje
        })

    df = pd.DataFrame(datos)

    st.metric("Participantes", len(df))

    mi_resultado = df[
        df["Estudiante"] == estudiante
    ]

    if not mi_resultado.empty:
        posicion = int(mi_resultado.iloc[0]["Puesto"])
        puntaje = int(
            mi_resultado.iloc[0]["Puntaje (%)"]
        )

        c1, c2 = st.columns(2)
        c1.metric("Mi posición", f"#{posicion}")
        c2.metric("Mi puntaje", f"{puntaje}%")

    st.subheader("Clasificación general")

    st.dataframe(
        df,
        hide_index=True,
        width="stretch"
    )

    st.caption(
        "Ranking del prototipo. Los resultados "
        "se ordenan por puntaje y fecha de registro."
    )
