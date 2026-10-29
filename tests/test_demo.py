import tempfile
import unittest
from pathlib import Path

from modulos import base_datos
from modulos.demo import (
    NOMBRE_DEMO,
    UNIVERSIDAD_DEMO,
    preparar_datos_demo
)


class DatosDemostracionTests(unittest.TestCase):
    def setUp(self):
        self.temporal = tempfile.TemporaryDirectory()
        self.ruta_original = base_datos.RUTA_DB
        base_datos.RUTA_DB = Path(self.temporal.name) / "demo.db"

    def tearDown(self):
        base_datos.RUTA_DB = self.ruta_original
        self.temporal.cleanup()

    def _conteo(self, tabla):
        with base_datos.conectar() as conexion:
            return conexion.execute(
                f"SELECT COUNT(*) FROM {tabla}"
            ).fetchone()[0]

    def test_creacion_es_idempotente(self):
        identidad = preparar_datos_demo()
        self.assertEqual(identidad, (NOMBRE_DEMO, UNIVERSIDAD_DEMO))
        self.assertEqual(self._conteo("progreso_estudiante"), 1)
        self.assertEqual(self._conteo("examenes_semanales"), 2)
        self.assertEqual(self._conteo("respuestas_examen"), 20)
        self.assertEqual(self._conteo("resultados"), 2)

        preparar_datos_demo()
        self.assertEqual(self._conteo("progreso_estudiante"), 1)
        self.assertEqual(self._conteo("examenes_semanales"), 2)
        self.assertEqual(self._conteo("respuestas_examen"), 20)
        self.assertEqual(self._conteo("resultados"), 2)

    def test_reinicio_restaura_el_perfil(self):
        preparar_datos_demo()
        with base_datos.conectar() as conexion:
            conexion.execute("""
                UPDATE progreso_estudiante
                SET puntos = 999
                WHERE estudiante = ? AND universidad = ?
            """, (NOMBRE_DEMO, UNIVERSIDAD_DEMO))

        preparar_datos_demo(reiniciar=True)
        puntos, historial, errores = base_datos.cargar_progreso(
            NOMBRE_DEMO, UNIVERSIDAD_DEMO
        )
        self.assertEqual(puntos, 30)
        self.assertTrue(historial)
        self.assertEqual(errores["Fracciones"], 2)


if __name__ == "__main__":
    unittest.main()
