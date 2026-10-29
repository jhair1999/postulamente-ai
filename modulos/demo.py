import json
from datetime import datetime, timedelta, timezone

from datos.preguntas import PREGUNTAS
from modulos.base_datos import (
    conectar,
    iniciar_base_datos,
    obtener_mes
)


NOMBRE_DEMO = "Estudiante Demo"
UNIVERSIDAD_DEMO = "UNMSM"
ESTUDIANTES_DEMO = (
    NOMBRE_DEMO,
    "Camila Demo",
    "Diego Demo"
)


HISTORIAL_DEMO = {
    1: {
        "intentos": 1,
        "resuelta": True,
        "materia": "Álgebra",
        "tema": "Ecuaciones de primer grado",
        "dificultad": "Básico",
        "pistas_usadas": 0,
        "errores": 0,
        "clasificacion": "dominio"
    },
    2: {
        "intentos": 2,
        "resuelta": True,
        "materia": "Álgebra",
        "tema": "Ecuaciones de primer grado",
        "dificultad": "Básico",
        "pistas_usadas": 0,
        "errores": 1,
        "clasificacion": "procedimiento_en_desarrollo"
    },
    3: {
        "intentos": 1,
        "resuelta": True,
        "materia": "Aritmética",
        "tema": "Porcentajes",
        "dificultad": "Básico",
        "pistas_usadas": 1,
        "errores": 0,
        "clasificacion": "dominio_con_pista"
    },
    4: {
        "intentos": 2,
        "resuelta": False,
        "materia": "Aritmética",
        "tema": "Fracciones",
        "dificultad": "Intermedio",
        "pistas_usadas": 1,
        "errores": 2,
        "clasificacion": "desconoce_tema"
    },
    13: {
        "intentos": 1,
        "resuelta": True,
        "materia": "Geometría",
        "tema": "Área de rectángulos",
        "dificultad": "Básico",
        "pistas_usadas": 0,
        "errores": 0,
        "clasificacion": "dominio"
    }
}

ERRORES_DEMO = {
    "Ecuaciones de primer grado": 1,
    "Fracciones": 2
}


def _respuesta_incorrecta(pregunta):
    return next(
        opcion
        for opcion in pregunta["opciones"]
        if opcion != pregunta["respuesta"]
    )


def _insertar_examen_demo(
    conexion,
    intento_id,
    preguntas,
    correctas,
    fecha
):
    respuestas = {}
    for indice, pregunta in enumerate(preguntas):
        respuestas[pregunta["id"]] = (
            pregunta["respuesta"]
            if indice < correctas
            else _respuesta_incorrecta(pregunta)
        )

    puntaje = round(correctas / len(preguntas) * 100)
    final = fecha + timedelta(minutes=8)
    conexion.execute("""
        INSERT OR IGNORE INTO intentos_examen
        (id, estudiante, universidad, tipo_examen, modalidad,
         convocatoria, estado, inicio, fin, finalizado_en,
         puntaje, correctas, total, preguntas_json, respuestas_json)
        VALUES (?, ?, ?, 'Semanal', 'oficial', ?, 'finalizado',
                ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        intento_id,
        NOMBRE_DEMO,
        UNIVERSIDAD_DEMO,
        f"demo-{intento_id}",
        fecha.isoformat(),
        final.isoformat(),
        final.isoformat(),
        puntaje,
        correctas,
        len(preguntas),
        json.dumps(preguntas, ensure_ascii=False),
        json.dumps(respuestas, ensure_ascii=False)
    ))
    conexion.execute("""
        INSERT OR IGNORE INTO examenes_semanales
        (estudiante, universidad, puntaje, correctas,
         total, fecha, intento_id)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        NOMBRE_DEMO,
        UNIVERSIDAD_DEMO,
        puntaje,
        correctas,
        len(preguntas),
        final.isoformat(),
        intento_id
    ))

    for indice, pregunta in enumerate(preguntas):
        respuesta = respuestas[pregunta["id"]]
        conexion.execute("""
            INSERT OR IGNORE INTO respuestas_examen
            (intento_id, estudiante, universidad, tipo_examen,
             pregunta_id, materia, tema, dificultad, respuesta,
             correcta, uso_pista, fecha)
            VALUES (?, ?, ?, 'Semanal', ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            intento_id,
            NOMBRE_DEMO,
            UNIVERSIDAD_DEMO,
            pregunta["id"],
            pregunta["materia"],
            pregunta["tema"],
            pregunta["dificultad"],
            respuesta,
            int(indice < correctas),
            int(indice == 2),
            final.isoformat()
        ))


def _insertar_competidor(conexion, nombre, puntaje, posicion):
    convocatoria = obtener_mes()
    intento_id = (
        f"demo-ranking-{convocatoria}-{nombre.lower().replace(' ', '-')}"
    )
    fecha = datetime.now(timezone.utc) - timedelta(days=posicion)
    correctas = round(len(PREGUNTAS) * puntaje / 100)
    conexion.execute("""
        INSERT OR IGNORE INTO intentos_examen
        (id, estudiante, universidad, tipo_examen, modalidad,
         convocatoria, estado, inicio, fin, finalizado_en,
         puntaje, correctas, total, preguntas_json, respuestas_json)
        VALUES (?, ?, ?, 'Mensual', 'oficial', ?, 'finalizado',
                ?, ?, ?, ?, ?, ?, '[]', '{}')
    """, (
        intento_id,
        nombre,
        UNIVERSIDAD_DEMO,
        convocatoria,
        fecha.isoformat(),
        fecha.isoformat(),
        fecha.isoformat(),
        puntaje,
        correctas,
        len(PREGUNTAS)
    ))
    conexion.execute("""
        INSERT OR IGNORE INTO resultados
        (estudiante, universidad, convocatoria, puntaje, fecha, intento_id)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        nombre,
        UNIVERSIDAD_DEMO,
        convocatoria,
        puntaje,
        fecha.isoformat(),
        intento_id
    ))


def _eliminar_datos_demo(conexion):
    marcadores = ",".join("?" for _ in ESTUDIANTES_DEMO)
    conexion.execute(
        f"DELETE FROM respuestas_examen WHERE estudiante IN ({marcadores})",
        ESTUDIANTES_DEMO
    )
    conexion.execute(
        f"DELETE FROM resultados WHERE estudiante IN ({marcadores})",
        ESTUDIANTES_DEMO
    )
    conexion.execute(
        f"DELETE FROM examenes_semanales WHERE estudiante IN ({marcadores})",
        ESTUDIANTES_DEMO
    )
    conexion.execute(
        f"DELETE FROM intentos_examen WHERE estudiante IN ({marcadores})",
        ESTUDIANTES_DEMO
    )
    conexion.execute(
        f"DELETE FROM progreso_estudiante WHERE estudiante IN ({marcadores})",
        ESTUDIANTES_DEMO
    )


def preparar_datos_demo(reiniciar=False):
    """Crea datos ficticios e idempotentes para una exposición."""
    iniciar_base_datos()
    ahora = datetime.now(timezone.utc)
    with conectar() as conexion:
        conexion.execute("BEGIN IMMEDIATE")
        if reiniciar:
            _eliminar_datos_demo(conexion)

        conexion.execute("""
            INSERT OR IGNORE INTO progreso_estudiante
            (estudiante, universidad, puntos, historial, errores)
            VALUES (?, ?, ?, ?, ?)
        """, (
            NOMBRE_DEMO,
            UNIVERSIDAD_DEMO,
            30,
            json.dumps(HISTORIAL_DEMO, ensure_ascii=False),
            json.dumps(ERRORES_DEMO, ensure_ascii=False)
        ))

        _insertar_examen_demo(
            conexion,
            "demo-semanal-1",
            PREGUNTAS[:10],
            6,
            ahora - timedelta(days=14)
        )
        _insertar_examen_demo(
            conexion,
            "demo-semanal-2",
            PREGUNTAS[10:20],
            8,
            ahora - timedelta(days=7)
        )
        _insertar_competidor(conexion, "Camila Demo", 87, 2)
        _insertar_competidor(conexion, "Diego Demo", 73, 1)

    return NOMBRE_DEMO, UNIVERSIDAD_DEMO
