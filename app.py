
import streamlit as st
from modulos.progreso import obtener_estadisticas
from modulos.aprendizaje import mostrar_aprendizaje
from modulos.estadisticas import mostrar_estadisticas
from modulos.agente import mostrar_agente
from modulos.examenes import mostrar_examen_semanal
from modulos.simulacro import mostrar_simulacro
from modulos.ranking import mostrar_ranking
from modulos.juegos import mostrar_juegos
from modulos.base_datos import cargar_progreso, iniciar_base_datos
from modulos.demo import (
    NOMBRE_DEMO,
    UNIVERSIDAD_DEMO,
    preparar_datos_demo
)

st.set_page_config(
    page_title="PostulaMente AI",
    page_icon="🎓",
    layout="wide"
)

iniciar_base_datos()

st.markdown("""
<style>
    [data-testid="stMetric"] {
        background: rgba(74, 98, 220, 0.08);
        border: 1px solid rgba(74, 98, 220, 0.18);
        border-radius: 14px;
        padding: 14px;
    }
    .block-container {padding-top: 2rem; padding-bottom: 3rem;}
</style>
""", unsafe_allow_html=True)

if "nombre" not in st.session_state:
    st.session_state.nombre = ""

if "universidad" not in st.session_state:
    st.session_state.universidad = ""

st.title("🎓 PostulaMente AI")
st.write("Tu academia preuniversitaria inteligente")

if st.session_state.nombre == "":
    st.subheader("¡Bienvenido!")

    nombre = st.text_input("¿Cómo te llamas?")

    universidad = st.selectbox(
        "¿A qué universidad quieres postular?",
        ["UNMSM", "UNI", "UNCP", "UNFV", "Otra"]
    )

    if st.button("Comenzar"):
        if nombre.strip():
            st.session_state.nombre = nombre.strip()
            st.session_state.universidad = universidad
            st.rerun()
        else:
            st.warning("Ingresa tu nombre.")

    st.divider()
    st.subheader("🎤 Presentación universitaria")
    st.write(
        "Abre un perfil ficticio con progreso, evaluaciones y "
        "competidores preparados para demostrar el sistema."
    )
    if st.button("🧪 Entrar al modo demostración", type="secondary"):
        nombre_demo, universidad_demo = preparar_datos_demo()
        st.session_state.nombre = nombre_demo
        st.session_state.universidad = universidad_demo
        st.session_state.modo_demo = True
        st.rerun()

else:
    
    identidad = (
        st.session_state.nombre,
        st.session_state.universidad
    )

    if st.session_state.get("perfil_cargado") != identidad:
        puntos, historial, errores = cargar_progreso(
            st.session_state.nombre,
            st.session_state.universidad
        )

        st.session_state.puntos = puntos
        st.session_state.historial = historial
        st.session_state.errores = errores
        st.session_state.perfil_cargado = identidad

    st.sidebar.title("📚 Menú principal")

    opcion = st.sidebar.radio(
        "Selecciona una opción:",
        [
            "Inicio",
            "Aprender teoría",
            "Practicar jugando",
            "Tutor inteligente",
            "Examen semanal",
            "Simulacro mensual",
            "Mi progreso",
            "Ranking"
        ]
    )

    st.sidebar.write(
        "Universidad:",
        st.session_state.universidad
    )

    if (
        st.session_state.nombre == NOMBRE_DEMO
        and st.session_state.universidad == UNIVERSIDAD_DEMO
    ):
        st.sidebar.success("🧪 Modo demostración")
        if st.sidebar.button("Restablecer demostración"):
            preparar_datos_demo(reiniciar=True)
            for clave in list(st.session_state.keys()):
                del st.session_state[clave]
            st.session_state.nombre = NOMBRE_DEMO
            st.session_state.universidad = UNIVERSIDAD_DEMO
            st.session_state.modo_demo = True
            st.rerun()

    if st.sidebar.button("Cerrar sesión"):
        for clave in list(st.session_state.keys()):
            del st.session_state[clave]
        st.rerun()

    if opcion == "Inicio":
        st.header(
            f"¡Hola, {st.session_state.nombre}! 👋"
        )
        st.success("¡Comencemos tu preparación!")

        puntos, nivel, porcentaje = obtener_estadisticas()

        c1, c2, c3 = st.columns(3)
        c1.metric("Nivel", nivel)
        c2.metric("Puntos", puntos)
        c3.metric("Ejercicios completados", f"{porcentaje}%")


    elif opcion == "Aprender teoría":
        mostrar_aprendizaje()

    elif opcion == "Practicar jugando":
        mostrar_juegos()

    
    elif opcion == "Tutor inteligente":
        mostrar_agente()


    
    elif opcion == "Examen semanal":
        mostrar_examen_semanal()


    elif opcion == "Simulacro mensual":
        mostrar_simulacro()

    
    elif opcion == "Mi progreso":
        mostrar_estadisticas()


    elif opcion == "Ranking":
        mostrar_ranking()
