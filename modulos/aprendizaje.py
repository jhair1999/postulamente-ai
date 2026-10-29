
import streamlit as st
from datos.preguntas import PREGUNTAS
from modulos.explicaciones import explicar_porcentaje
from modulos.progreso import registrar_respuesta


def mostrar_aprendizaje():
    st.header("📚 Aprende matemáticas")
    st.write("Selecciona una materia para comenzar.")

    materias = sorted(set(
        pregunta["materia"] for pregunta in PREGUNTAS
    ))

    materia = st.selectbox(
        "Selecciona una materia:",
        materias
    )

    preguntas = [
        p for p in PREGUNTAS
        if p["materia"] == materia
    ]

    temas = sorted(set(p["tema"] for p in preguntas))

    tema = st.selectbox(
        "Selecciona un tema:",
        temas
    )

    st.subheader(f"📖 {tema}")

    if tema == "Ecuaciones de primer grado":
        st.info(
            "Una ecuación es una igualdad que contiene "
            "una incógnita. Para resolverla debemos "
            "encontrar su valor."
        )
        st.latex(r"2x + 6 = 16")
        st.write("Restamos 6 y dividimos entre 2.")
        st.latex(r"x = \frac{16-6}{2} = 5")

    elif tema == "Porcentajes":
        st.info(
            "Un porcentaje representa una cantidad "
            "de cada 100 unidades."
        )
        st.latex(r"20\% \times 150 = 30")

    else:
        ejemplo = next(p for p in preguntas if p["tema"] == tema)
        st.info(
            f"Método principal: {ejemplo['metodo']}. "
            "Lee los pasos del ejemplo y comprueba cada operación."
        )
        st.write(
            "**Conocimientos previos:** "
            + ", ".join(ejemplo["prerrequisitos"])
        )

    st.divider()
    st.subheader("🎮 Practica lo aprendido")

    disponibles = [
        p for p in preguntas if p["tema"] == tema
    ]

    numero = st.selectbox(
        "Selecciona un ejercicio:",
        range(len(disponibles)),
        format_func=lambda i: f"Ejercicio {i + 1}"
    )

    ejercicio = disponibles[numero]

    st.write(f"**{ejercicio['pregunta']}**")

    respuesta = st.radio(
        "Selecciona tu respuesta:",
        ejercicio["opciones"],
        index=None,
        key=f"respuesta_{ejercicio['id']}"
    )

    if st.button(
        "Comprobar respuesta",
        key=f"comprobar_{ejercicio['id']}"
    ):
        if respuesta is None:
            st.warning("Selecciona una respuesta.")
        else:
            correcta, puntos, mensaje = registrar_respuesta(
                ejercicio, respuesta
            )

            
            if mensaje == "Esta pregunta ya fue completada.":
                st.info("ℹ️ Ya completaste este ejercicio. No se suman más puntos.")
            elif correcta:
                st.success(f"✅ {mensaje} +{puntos} puntos")
            else:
                st.error(f"❌ {mensaje}")


    with st.expander("🤖 Explicación paso a paso"):
        for i, paso in enumerate(
            ejercicio["explicacion"], start=1
        ):
            st.write(f"**Paso {i}:** {paso}")

    if tema == "Porcentajes":
        st.divider()

        if st.toggle("🎓 Activar explicación desde cero"):
            explicar_porcentaje()
