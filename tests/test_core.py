import sqlite3
import tempfile
import unittest
from contextlib import closing
from datetime import datetime, timedelta, timezone
from pathlib import Path

from datos.preguntas import PREGUNTAS
from modulos import base_datos


class BancoPreguntasTests(unittest.TestCase):
    def test_banco_tiene_30_preguntas_validas(self):
        campos = {
            "id", "materia", "tema", "dificultad", "pregunta",
            "opciones", "respuesta", "explicacion", "prerrequisitos",
            "pistas", "metodo"
        }
        self.assertGreaterEqual(len(PREGUNTAS), 30)
        self.assertEqual(
            len({pregunta["id"] for pregunta in PREGUNTAS}),
            len(PREGUNTAS)
        )
        for pregunta in PREGUNTAS:
            self.assertTrue(campos.issubset(pregunta))
            self.assertIn(pregunta["respuesta"], pregunta["opciones"])
            self.assertGreaterEqual(len(pregunta["explicacion"]), 2)


class PersistenciaIntentosTests(unittest.TestCase):
    def setUp(self):
        self.temporal = tempfile.TemporaryDirectory()
        self.ruta_original = base_datos.RUTA_DB
        base_datos.RUTA_DB = Path(self.temporal.name) / "prueba.db"
        base_datos.iniciar_base_datos()
        self.preguntas = PREGUNTAS[:2]

    def tearDown(self):
        base_datos.RUTA_DB = self.ruta_original
        self.temporal.cleanup()

    def _conteo(self, tabla):
        with base_datos.conectar() as conexion:
            return conexion.execute(
                f"SELECT COUNT(*) FROM {tabla}"
            ).fetchone()[0]

    def test_finalizacion_oficial_es_atomica_e_idempotente(self):
        intento, creado = base_datos.crear_intento(
            "Ana", "UNMSM", "Mensual", "oficial",
            self.preguntas, 15, convocatoria="2099-01"
        )
        self.assertTrue(creado)
        self.assertTrue(base_datos.guardar_borrador_intento(
            intento["id"], {1: self.preguntas[0]["respuesta"]}
        ))
        final = base_datos.finalizar_intento(
            intento["id"], {2: self.preguntas[1]["respuesta"]}
        )
        self.assertEqual(final["estado"], "finalizado")
        self.assertEqual(final["puntaje"], 100)
        self.assertEqual(self._conteo("resultados"), 1)
        self.assertEqual(self._conteo("respuestas_examen"), 2)

        repetido = base_datos.finalizar_intento(intento["id"], {})
        self.assertEqual(repetido["puntaje"], 100)
        self.assertEqual(self._conteo("resultados"), 1)
        self.assertEqual(self._conteo("respuestas_examen"), 2)

    def test_un_solo_intento_oficial_por_convocatoria(self):
        primero, creado = base_datos.crear_intento(
            "Luis", "UNI", "Mensual", "oficial",
            self.preguntas, 15, convocatoria="2099-02"
        )
        segundo, creado_segundo = base_datos.crear_intento(
            "luis", "uni", "Mensual", "oficial",
            self.preguntas, 15, convocatoria="2099-02"
        )
        self.assertTrue(creado)
        self.assertFalse(creado_segundo)
        self.assertEqual(primero["id"], segundo["id"])

    def test_no_acepta_respuestas_despues_del_limite(self):
        inicio = datetime.now(timezone.utc) - timedelta(minutes=2)
        intento, _ = base_datos.crear_intento(
            "Rosa", "UNFV", "Mensual", "practica",
            self.preguntas, 1, inicio=inicio
        )
        durante = inicio + timedelta(seconds=30)
        self.assertTrue(base_datos.guardar_borrador_intento(
            intento["id"],
            {1: self.preguntas[0]["respuesta"]},
            ahora=durante
        ))
        self.assertFalse(base_datos.guardar_borrador_intento(
            intento["id"],
            {2: self.preguntas[1]["respuesta"]},
            ahora=datetime.now(timezone.utc)
        ))
        final = base_datos.finalizar_intento(
            intento["id"],
            {2: self.preguntas[1]["respuesta"]},
            ahora=datetime.now(timezone.utc)
        )
        self.assertEqual(final["correctas"], 1)
        self.assertNotIn(2, final["respuestas"])

    def test_practica_no_ingresa_al_ranking(self):
        intento, _ = base_datos.crear_intento(
            "Diego", "UNCP", "Mensual", "practica",
            self.preguntas, 15
        )
        base_datos.finalizar_intento(intento["id"], {})
        self.assertEqual(self._conteo("resultados"), 0)
        self.assertEqual(self._conteo("respuestas_examen"), 2)

    def test_esquema_e_integridad(self):
        with closing(sqlite3.connect(base_datos.RUTA_DB)) as conexion:
            self.assertEqual(
                conexion.execute("PRAGMA integrity_check").fetchone()[0],
                "ok"
            )
            tablas = {
                fila[0]
                for fila in conexion.execute(
                    "SELECT name FROM sqlite_master WHERE type='table'"
                )
            }
        self.assertTrue({
            "intentos_examen", "respuestas_examen", "resultados",
            "examenes_semanales", "progreso_estudiante"
        }.issubset(tablas))


if __name__ == "__main__":
    unittest.main()
