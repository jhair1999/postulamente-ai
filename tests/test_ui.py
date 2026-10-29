import tempfile
import unittest
from pathlib import Path

from streamlit.testing.v1 import AppTest

from modulos import base_datos


class InterfazTests(unittest.TestCase):
    def setUp(self):
        self.temporal = tempfile.TemporaryDirectory()
        self.ruta_original = base_datos.RUTA_DB
        base_datos.RUTA_DB = Path(self.temporal.name) / "interfaz.db"

    def tearDown(self):
        base_datos.RUTA_DB = self.ruta_original
        self.temporal.cleanup()

    def _iniciar_sesion(self, nombre="Prueba UI"):
        ruta_app = Path(__file__).resolve().parents[1] / "app.py"
        app = AppTest.from_file(str(ruta_app)).run(timeout=20)
        app.text_input[0].input(nombre)
        siguiente = next(
            boton for boton in app.button if boton.label == "Comenzar"
        )
        siguiente.click()
        app.run(timeout=20)
        self.assertEqual(len(app.exception), 0)
        return app

    def test_todas_las_paginas_cargan_sin_excepciones(self):
        app = self._iniciar_sesion()
        paginas = [
            "Inicio", "Aprender teoría", "Practicar jugando",
            "Tutor inteligente", "Examen semanal", "Simulacro mensual",
            "Mi progreso", "Ranking"
        ]
        for pagina in paginas:
            app.sidebar.radio[0].set_value(pagina)
            app.run(timeout=20)
            self.assertEqual(
                len(app.exception), 0,
                f"La página {pagina} produjo una excepción."
            )

    def test_examen_semanal_guarda_un_intento_completo(self):
        app = self._iniciar_sesion("Prueba Examen")
        app.sidebar.radio[0].set_value("Examen semanal")
        app.run(timeout=20)
        next(
            boton for boton in app.button
            if boton.label == "🚀 Comenzar examen"
        ).click()
        app.run(timeout=20)
        next(
            boton for boton in app.button
            if boton.label == "✅ Entregar examen"
        ).click()
        app.run(timeout=20)
        self.assertEqual(len(app.exception), 0)
        with base_datos.conectar() as conexion:
            examenes = conexion.execute(
                "SELECT COUNT(*) FROM examenes_semanales"
            ).fetchone()[0]
            respuestas = conexion.execute(
                "SELECT COUNT(*) FROM respuestas_examen"
            ).fetchone()[0]
        self.assertEqual(examenes, 1)
        self.assertEqual(respuestas, 10)

    def test_modo_demo_carga_y_se_puede_restaurar(self):
        ruta_app = Path(__file__).resolve().parents[1] / "app.py"
        app = AppTest.from_file(str(ruta_app)).run(timeout=20)
        next(
            boton for boton in app.button
            if boton.label == "🧪 Entrar al modo demostración"
        ).click()
        app.run(timeout=20)
        self.assertEqual(len(app.exception), 0)
        self.assertTrue(any(
            "Modo demostración" in elemento.value
            for elemento in app.sidebar.success
        ))

        next(
            boton for boton in app.sidebar.button
            if boton.label == "Restablecer demostración"
        ).click()
        app.run(timeout=20)
        self.assertEqual(len(app.exception), 0)
        puntos, _, _ = base_datos.cargar_progreso(
            "Estudiante Demo", "UNMSM"
        )
        self.assertEqual(puntos, 30)


if __name__ == "__main__":
    unittest.main()
