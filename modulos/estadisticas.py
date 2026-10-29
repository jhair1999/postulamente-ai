
import streamlit as st
import pandas as pd
from modulos.dominio import calcular_dominio
from modulos.progreso import (
    iniciar_progreso,
    obtener_estadisticas
)

from modulos.base_datos import (
    obtener_examenes_semanales,
    obtener_resumen_respuestas,
    conectar,
    iniciar_base_datos
)


def mostrar_estadisticas():
    iniciar_progreso()

    st.header("📊 Mi progreso académico")
    st.write(
        "Revisa tus prácticas, evaluaciones "
        "y temas que necesitas reforzar."
    )

    puntos, nivel, porcentaje = obtener_estadisticas()

    historial = st.session_state.historial
    errores = st.session_state.errores

    completadas = sum(
        1 for r in historial.values()
        if r["resuelta"]
    )

    c1, c2, c3, c4 = st.columns(4)

    c1.metric("Puntos XP", puntos)
    c2.metric("Nivel", nivel)
    c3.metric("Prácticas completadas", completadas)
    c4.metric("Prácticas completadas (%)", f"{porcentaje}%")

    st.divider()

    st.subheader("🧠 Mi nivel de preparación")

    dominio = calcular_dominio(
        st.session_state.nombre,
        st.session_state.universidad
    )

    if dominio["porcentaje"] is not None:
        valor = dominio["porcentaje"]

        st.metric(
            "Dominio académico estimado",
            f"{valor}%"
        )

        st.progress(valor / 100)

        st.write(f"**Nivel:** {dominio['nivel']}")

        st.info(
            f"🤖 {dominio['recomendacion']}"
        )

        st.caption(
            "Estimación provisional basada en evaluaciones. "
            "No representa una probabilidad de ingreso."
        )

    else:
        st.info(
            "Realiza un examen para obtener "
            "tu primera estimación."
        )

    st.divider()

    # PROGRESO POR MATERIA
    st.subheader("📚 Progreso por materia")

    if historial:
        materias = {}

        for registro in historial.values():
            materia = registro["materia"]

            if materia not in materias:
                materias[materia] = {
                    "intentadas": 0,
                    "completadas": 0
                }

            materias[materia]["intentadas"] += 1

            if registro["resuelta"]:
                materias[materia]["completadas"] += 1

        datos = []

        for materia, valores in materias.items():
            avance = round(
                valores["completadas"]
                / valores["intentadas"] * 100
            )

            datos.append({
                "Materia": materia,
                "Avance (%)": avance,
                "Completadas": valores["completadas"],
                "Intentadas": valores["intentadas"]
            })

        df = pd.DataFrame(datos)

        st.dataframe(
            df,
            hide_index=True,
            width="stretch"
        )

        st.bar_chart(
            df.set_index("Materia")["Avance (%)"],
            y_label="Porcentaje de prácticas completadas"
        )

    else:
        st.info(
            "Todavía no has realizado prácticas."
        )

    st.divider()

    # DIFICULTADES
    st.subheader("🔍 Dificultades detectadas")

    errores_totales = errores.copy()
    for registro in obtener_resumen_respuestas(
        st.session_state.nombre,
        st.session_state.universidad
    ):
        errores_totales[registro["tema"]] = (
            errores_totales.get(registro["tema"], 0)
            + registro["errores"]
        )

    if errores_totales:
        for tema, cantidad in sorted(
            errores_totales.items(),
            key=lambda x: x[1],
            reverse=True
        ):
            st.warning(
                f"{tema}: {cantidad} errores registrados"
            )

        tema_refuerzo = max(errores_totales, key=errores_totales.get)

        st.info(
            f"🤖 Te recomiendo reforzar: {tema_refuerzo}"
        )

    else:
        st.success(
            "No hay errores registrados en las prácticas."
        )

    st.divider()

    # EXAMENES SEMANALES
    st.subheader("📝 Historial de exámenes semanales")

    examenes = obtener_examenes_semanales(
        st.session_state.nombre,
        st.session_state.universidad
    )

    if examenes:
        df_examenes = pd.DataFrame(
            examenes,
            columns=[
                "Fecha",
                "Nota (%)",
                "Correctas",
                "Total"
            ]
        )

        df_examenes["Fecha"] = pd.to_datetime(
            df_examenes["Fecha"]
        ).dt.strftime("%d/%m/%Y")

        st.dataframe(
            df_examenes,
            hide_index=True,
            width="stretch"
        )

        promedio = round(
            df_examenes["Nota (%)"].mean()
        )

        st.metric("Promedio semanal", f"{promedio}%")

    else:
        st.info(
            "Todavía no tienes exámenes semanales guardados."
        )

    st.divider()

    # SIMULACROS MENSUALES
    st.subheader("🏆 Historial de simulacros mensuales")

    iniciar_base_datos()

    with conectar() as conexion:
        mensuales = conexion.execute("""
            SELECT convocatoria, puntaje
            FROM resultados
            WHERE estudiante = ?
              AND universidad = ?
            ORDER BY convocatoria DESC
        """, (
            st.session_state.nombre,
            st.session_state.universidad
        )).fetchall()

    if mensuales:
        df_mensual = pd.DataFrame(
            mensuales,
            columns=["Convocatoria", "Puntaje (%)"]
        )

        st.dataframe(
            df_mensual,
            hide_index=True,
            width="stretch"
        )

        st.metric(
            "Último simulacro mensual",
            f"{mensuales[0][1]}%"
        )

    else:
        st.info(
            "Todavía no tienes simulacros mensuales guardados."
        )
