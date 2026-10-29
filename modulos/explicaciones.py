
import streamlit as st


def explicar_porcentaje():
    st.subheader("🤖 Aprendamos desde cero")
    st.write("Vamos a calcular el 20% de 150.")

    st.markdown("### Paso 1. ¿Qué significa 20%?")
    st.write(
        "El símbolo % significa 'por cada 100'. "
        "Por eso escribimos:"
    )
    st.latex(r"20\% = \frac{20}{100}")

    with st.expander("🔎 ¿Por qué dividimos entre 100?"):
        st.write(
            "Porque un porcentaje representa partes de 100. "
            "20% significa 20 partes de un total de 100."
        )

    st.markdown("### Paso 2. Simplificamos la fracción")
    st.latex(r"\frac{20}{100} = \frac{2}{10} = \frac{1}{5}")

    with st.expander("🔎 ¿Cómo simplificamos?"):
        st.write(
            "Dividimos 20 y 100 entre 10. "
            "Obtenemos 2/10. Después dividimos "
            "2 y 10 entre 2. Obtenemos 1/5."
        )

    st.markdown("### Paso 3. Convertimos a decimal")
    st.latex(r"\frac{1}{5} = 0.2 = 0.20")

    with st.expander("🔎 ¿Cómo se hace la división?"):
        st.write(
            "Dividir 1 entre 5 da 0.2. "
            "Vamos a mostrarlo como una división "
            "tradicional de cuaderno."
        )

        st.code(
            "  1,0 | 5\n"
            " -0   |------\n"
            "  10  | 0,2\n"
            " -10\n"
            "   0",
            language=None
        )

        st.write(
            "Como 1 es menor que 5, escribimos 0 "
            "en el cociente y colocamos la coma decimal. "
            "Agregamos un cero y dividimos 10 entre 5. "
            "Como 5 cabe 2 veces en 10, obtenemos 0,2."
        )

    st.markdown("### Paso 4. Calculamos el resultado")
    st.latex(r"0.20 \times 150 = 30")

    with st.expander("🔎 ¿Por qué multiplicamos por 150?"):
        st.write(
            "Porque queremos encontrar 20 partes "
            "de cada 100 de la cantidad 150."
        )
        st.latex(r"\frac{20 \times 150}{100} = 30")

    st.success("✅ Respuesta final: 30")
