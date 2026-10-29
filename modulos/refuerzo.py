
import streamlit as st


def mostrar_refuerzo(tema):
    st.divider()
    st.subheader(f"📖 Clase de refuerzo: {tema}")

    if tema == "Operaciones básicas":
        st.write(
            "Antes de resolver ecuaciones, debemos "
            "comprender las operaciones matemáticas."
        )

        st.markdown("### ¿Qué es sumar?")
        st.write("Sumar significa juntar cantidades.")
        st.latex(r"3 + 2 = 5")

        with st.expander("🔎 ¿Por qué 3 + 2 = 5?"):
            st.write(
                "Si tienes 3 objetos y agregas otros 2, "
                "terminas teniendo 5 objetos."
            )

        st.markdown("### ¿Qué es restar?")
        st.write("Restar significa quitar una cantidad.")
        st.latex(r"8 - 3 = 5")

        with st.expander("🔎 ¿Cómo se hace la resta?"):
            st.write(
                "Comenzamos con 8 unidades y quitamos 3. "
                "Nos quedan 5 unidades."
            )

    elif tema == "Números negativos":
        st.write(
            "Los números negativos representan valores "
            "menores que cero."
        )
        st.latex(r"-5 < 0")

        with st.expander("🔎 Ejemplo desde cero"):
            st.write(
                "Si tienes 0 soles y debes 5 soles, "
                "tu balance es -5 soles."
            )

    elif tema == "Despeje de incógnitas":
        st.write(
            "Despejar significa dejar sola la incógnita "
            "para encontrar su valor."
        )

        st.latex(r"x + 4 = 10")
        st.write("Restamos 4 a ambos lados:")
        st.latex(r"x = 10 - 4")
        st.latex(r"x = 6")

        with st.expander("🔎 ¿Por qué restamos 4?"):
            st.write(
                "Porque debemos mantener el equilibrio "
                "de la ecuación. Restamos 4 en ambos lados "
                "para dejar sola la x."
            )

    elif tema == "Fracciones":
        st.write(
            "Una fracción representa una parte de un todo."
        )
        st.latex(r"\frac{1}{2}")

    elif tema == "Divisiones":
        st.write(
            "Dividir significa repartir una cantidad "
            "en partes iguales."
        )
        st.latex(r"10 \div 2 = 5")

    elif tema == "Multiplicaciones":
        st.write(
            "Multiplicar es una forma abreviada "
            "de realizar sumas repetidas."
        )
        st.latex(r"3 \times 4 = 12")

    else:
        st.info("Esta lección estará disponible próximamente.")
