import json
import sqlite3
import uuid
from datetime import datetime, timedelta, timezone
from pathlib import Path
from zoneinfo import ZoneInfo


RUTA_DB = Path(__file__).resolve().parent.parent / "datos" / "postulamente.db"
ZONA_LIMA = ZoneInfo("America/Lima")
TIPOS_EXAMEN = {"Semanal", "Mensual"}
MODALIDADES = {"oficial", "practica"}


class ConexionSQLite(sqlite3.Connection):
    """Confirma o revierte la transacción y siempre libera el archivo."""

    def __exit__(self, exc_type, exc_value, traceback):
        try:
            return super().__exit__(exc_type, exc_value, traceback)
        finally:
            self.close()


def conectar():
    conexion = sqlite3.connect(
        RUTA_DB, timeout=10, factory=ConexionSQLite
    )
    conexion.execute("PRAGMA foreign_keys = ON")
    conexion.execute("PRAGMA busy_timeout = 10000")
    return conexion


def _ahora_utc():
    return datetime.now(timezone.utc)


def _como_utc(valor):
    if valor is None:
        return _ahora_utc()
    if valor.tzinfo is None:
        return valor.replace(tzinfo=timezone.utc)
    return valor.astimezone(timezone.utc)


def _columnas(conexion, tabla):
    return {
        fila[1]
        for fila in conexion.execute(f"PRAGMA table_info({tabla})").fetchall()
    }


def _agregar_columna(conexion, tabla, nombre, definicion):
    if nombre not in _columnas(conexion, tabla):
        conexion.execute(
            f"ALTER TABLE {tabla} ADD COLUMN {nombre} {definicion}"
        )


def obtener_mes():
    return datetime.now(ZONA_LIMA).strftime("%Y-%m")


def obtener_semana():
    ahora = datetime.now(ZONA_LIMA)
    anio, semana, _ = ahora.isocalendar()
    return f"{anio}-S{semana:02d}"


def iniciar_base_datos():
    """Crea y migra el esquema sin eliminar información existente."""
    RUTA_DB.parent.mkdir(parents=True, exist_ok=True)

    with conectar() as conexion:
        conexion.execute("PRAGMA journal_mode = WAL")
        conexion.execute("""
            CREATE TABLE IF NOT EXISTS resultados (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                estudiante TEXT NOT NULL,
                universidad TEXT NOT NULL,
                convocatoria TEXT NOT NULL,
                puntaje INTEGER NOT NULL,
                fecha TEXT NOT NULL,
                intento_id TEXT,
                UNIQUE(estudiante, universidad, convocatoria)
            )
        """)
        _agregar_columna(conexion, "resultados", "intento_id", "TEXT")

        conexion.execute("""
            CREATE TABLE IF NOT EXISTS progreso_estudiante (
                estudiante TEXT NOT NULL,
                universidad TEXT NOT NULL,
                puntos INTEGER NOT NULL DEFAULT 0,
                historial TEXT NOT NULL DEFAULT '{}',
                errores TEXT NOT NULL DEFAULT '{}',
                PRIMARY KEY (estudiante, universidad)
            )
        """)

        conexion.execute("""
            CREATE TABLE IF NOT EXISTS examenes_semanales (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                estudiante TEXT NOT NULL,
                universidad TEXT NOT NULL,
                puntaje INTEGER NOT NULL,
                correctas INTEGER NOT NULL,
                total INTEGER NOT NULL,
                fecha TEXT NOT NULL,
                intento_id TEXT
            )
        """)
        _agregar_columna(
            conexion, "examenes_semanales", "intento_id", "TEXT"
        )

        conexion.execute("""
            CREATE TABLE IF NOT EXISTS intentos_examen (
                id TEXT PRIMARY KEY,
                estudiante TEXT COLLATE NOCASE NOT NULL,
                universidad TEXT COLLATE NOCASE NOT NULL,
                tipo_examen TEXT NOT NULL,
                modalidad TEXT NOT NULL,
                convocatoria TEXT,
                estado TEXT NOT NULL DEFAULT 'en_curso',
                inicio TEXT NOT NULL,
                fin TEXT NOT NULL,
                finalizado_en TEXT,
                puntaje INTEGER,
                correctas INTEGER,
                total INTEGER NOT NULL,
                preguntas_json TEXT NOT NULL,
                respuestas_json TEXT NOT NULL DEFAULT '{}',
                CHECK (tipo_examen IN ('Semanal', 'Mensual')),
                CHECK (modalidad IN ('oficial', 'practica')),
                CHECK (estado IN ('en_curso', 'finalizado'))
            )
        """)

        conexion.execute("""
            CREATE TABLE IF NOT EXISTS respuestas_examen (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                intento_id TEXT,
                estudiante TEXT NOT NULL,
                universidad TEXT NOT NULL,
                tipo_examen TEXT NOT NULL,
                pregunta_id INTEGER NOT NULL,
                materia TEXT NOT NULL,
                tema TEXT NOT NULL,
                dificultad TEXT NOT NULL DEFAULT 'No registrada',
                respuesta TEXT,
                correcta INTEGER NOT NULL,
                uso_pista INTEGER NOT NULL DEFAULT 0,
                fecha TEXT NOT NULL,
                FOREIGN KEY (intento_id) REFERENCES intentos_examen(id)
            )
        """)
        _agregar_columna(
            conexion, "respuestas_examen", "intento_id", "TEXT"
        )
        _agregar_columna(
            conexion,
            "respuestas_examen",
            "dificultad",
            "TEXT NOT NULL DEFAULT 'No registrada'"
        )
        _agregar_columna(
            conexion,
            "respuestas_examen",
            "uso_pista",
            "INTEGER NOT NULL DEFAULT 0"
        )

        # Convertimos los resultados anteriores en intentos finalizados.
        for fila in conexion.execute("""
            SELECT id, estudiante, universidad, convocatoria, puntaje, fecha
            FROM resultados
            WHERE intento_id IS NULL
        """).fetchall():
            resultado_id, estudiante, universidad, convocatoria, puntaje, fecha = fila
            intento_id = f"legacy-mensual-{resultado_id}"
            conexion.execute("""
                INSERT OR IGNORE INTO intentos_examen
                (id, estudiante, universidad, tipo_examen, modalidad,
                 convocatoria, estado, inicio, fin, finalizado_en,
                 puntaje, correctas, total, preguntas_json, respuestas_json)
                VALUES (?, ?, ?, 'Mensual', 'oficial', ?, 'finalizado',
                        ?, ?, ?, ?, NULL, 0, '[]', '{}')
            """, (
                intento_id, estudiante, universidad, convocatoria,
                fecha, fecha, fecha, puntaje
            ))
            conexion.execute(
                "UPDATE resultados SET intento_id = ? WHERE id = ?",
                (intento_id, resultado_id)
            )

        for fila in conexion.execute("""
            SELECT id, estudiante, universidad, puntaje,
                   correctas, total, fecha
            FROM examenes_semanales
            WHERE intento_id IS NULL
        """).fetchall():
            examen_id, estudiante, universidad, puntaje, correctas, total, fecha = fila
            intento_id = f"legacy-semanal-{examen_id}"
            conexion.execute("""
                INSERT OR IGNORE INTO intentos_examen
                (id, estudiante, universidad, tipo_examen, modalidad,
                 convocatoria, estado, inicio, fin, finalizado_en,
                 puntaje, correctas, total, preguntas_json, respuestas_json)
                VALUES (?, ?, ?, 'Semanal', 'oficial', NULL, 'finalizado',
                        ?, ?, ?, ?, ?, ?, '[]', '{}')
            """, (
                intento_id, estudiante, universidad,
                fecha, fecha, fecha, puntaje, correctas, total
            ))
            conexion.execute(
                "UPDATE examenes_semanales SET intento_id = ? WHERE id = ?",
                (intento_id, examen_id)
            )

        conexion.execute("""
            CREATE UNIQUE INDEX IF NOT EXISTS uq_intento_mensual_oficial
            ON intentos_examen(estudiante, universidad, convocatoria)
            WHERE tipo_examen = 'Mensual' AND modalidad = 'oficial'
        """)
        conexion.execute("""
            CREATE UNIQUE INDEX IF NOT EXISTS uq_respuesta_intento_pregunta
            ON respuestas_examen(intento_id, pregunta_id)
            WHERE intento_id IS NOT NULL
        """)
        conexion.execute("""
            CREATE UNIQUE INDEX IF NOT EXISTS uq_resultado_intento
            ON resultados(intento_id)
            WHERE intento_id IS NOT NULL
        """)
        conexion.execute("""
            CREATE UNIQUE INDEX IF NOT EXISTS uq_examen_semanal_intento
            ON examenes_semanales(intento_id)
            WHERE intento_id IS NOT NULL
        """)


def _normalizar_identidad(estudiante, universidad):
    estudiante = str(estudiante).strip()
    universidad = str(universidad).strip()
    if not estudiante or not universidad:
        raise ValueError("El estudiante y la universidad son obligatorios.")
    return estudiante, universidad


def _fila_intento(fila):
    if fila is None:
        return None
    datos = dict(fila)
    datos["preguntas"] = json.loads(datos.pop("preguntas_json"))
    datos["respuestas"] = {
        int(k): v
        for k, v in json.loads(
            datos.pop("respuestas_json") or "{}"
        ).items()
    }
    datos["inicio"] = datetime.fromisoformat(datos["inicio"])
    datos["fin"] = datetime.fromisoformat(datos["fin"])
    if datos.get("finalizado_en"):
        datos["finalizado_en"] = datetime.fromisoformat(
            datos["finalizado_en"]
        )
    return datos


def _seleccionar_intento(conexion, intento_id):
    conexion.row_factory = sqlite3.Row
    return conexion.execute(
        "SELECT * FROM intentos_examen WHERE id = ?", (intento_id,)
    ).fetchone()


def crear_intento(
    estudiante,
    universidad,
    tipo_examen,
    modalidad,
    preguntas,
    duracion_minutos,
    convocatoria=None,
    inicio=None
):
    iniciar_base_datos()
    estudiante, universidad = _normalizar_identidad(
        estudiante, universidad
    )
    if tipo_examen not in TIPOS_EXAMEN:
        raise ValueError("Tipo de examen no válido.")
    if modalidad not in MODALIDADES:
        raise ValueError("Modalidad no válida.")
    if not preguntas:
        raise ValueError("El intento necesita al menos una pregunta.")
    if duracion_minutos <= 0:
        raise ValueError("La duración debe ser positiva.")

    if tipo_examen == "Mensual" and modalidad == "oficial":
        convocatoria = convocatoria or obtener_mes()
    elif tipo_examen == "Semanal" and convocatoria is None:
        convocatoria = obtener_semana()

    inicio = _como_utc(inicio)
    fin = inicio + timedelta(minutes=duracion_minutos)
    intento_id = str(uuid.uuid4())
    preguntas_json = json.dumps(
        preguntas, ensure_ascii=False, separators=(",", ":")
    )

    with conectar() as conexion:
        conexion.execute("BEGIN IMMEDIATE")
        conexion.row_factory = sqlite3.Row
        if tipo_examen == "Mensual" and modalidad == "oficial":
            existente = conexion.execute("""
                SELECT * FROM intentos_examen
                WHERE estudiante = ? COLLATE NOCASE
                  AND universidad = ? COLLATE NOCASE
                  AND tipo_examen = 'Mensual'
                  AND modalidad = 'oficial'
                  AND convocatoria = ?
                LIMIT 1
            """, (estudiante, universidad, convocatoria)).fetchone()
            if existente is not None:
                return _fila_intento(existente), False

        conexion.execute("""
            INSERT INTO intentos_examen
            (id, estudiante, universidad, tipo_examen, modalidad,
             convocatoria, estado, inicio, fin, total,
             preguntas_json, respuestas_json)
            VALUES (?, ?, ?, ?, ?, ?, 'en_curso', ?, ?, ?, ?, '{}')
        """, (
            intento_id, estudiante, universidad, tipo_examen, modalidad,
            convocatoria, inicio.isoformat(), fin.isoformat(),
            len(preguntas), preguntas_json
        ))
        fila = _seleccionar_intento(conexion, intento_id)

    return _fila_intento(fila), True


def obtener_intento(intento_id):
    iniciar_base_datos()
    with conectar() as conexion:
        fila = _seleccionar_intento(conexion, intento_id)
    return _fila_intento(fila)


def obtener_intento_activo(
    estudiante,
    universidad,
    tipo_examen,
    modalidad=None,
    convocatoria=None
):
    iniciar_base_datos()
    condiciones = [
        "estudiante = ? COLLATE NOCASE",
        "universidad = ? COLLATE NOCASE",
        "tipo_examen = ?",
        "estado = 'en_curso'"
    ]
    parametros = [estudiante.strip(), universidad.strip(), tipo_examen]
    if modalidad:
        condiciones.append("modalidad = ?")
        parametros.append(modalidad)
    if convocatoria:
        condiciones.append("convocatoria = ?")
        parametros.append(convocatoria)

    consulta = f"""
        SELECT * FROM intentos_examen
        WHERE {' AND '.join(condiciones)}
        ORDER BY inicio DESC
        LIMIT 1
    """
    with conectar() as conexion:
        conexion.row_factory = sqlite3.Row
        fila = conexion.execute(consulta, parametros).fetchone()
    return _fila_intento(fila)


def obtener_simulacro_oficial(estudiante, universidad, convocatoria=None):
    iniciar_base_datos()
    convocatoria = convocatoria or obtener_mes()
    with conectar() as conexion:
        conexion.row_factory = sqlite3.Row
        fila = conexion.execute("""
            SELECT * FROM intentos_examen
            WHERE estudiante = ? COLLATE NOCASE
              AND universidad = ? COLLATE NOCASE
              AND tipo_examen = 'Mensual'
              AND modalidad = 'oficial'
              AND convocatoria = ?
            LIMIT 1
        """, (
            estudiante.strip(), universidad.strip(), convocatoria
        )).fetchone()
    return _fila_intento(fila)


def _respuestas_validas(preguntas, respuestas):
    preguntas_por_id = {
        int(pregunta["id"]): pregunta for pregunta in preguntas
    }
    validas = {}
    for clave, respuesta in (respuestas or {}).items():
        try:
            pregunta_id = int(clave)
        except (TypeError, ValueError):
            continue
        pregunta = preguntas_por_id.get(pregunta_id)
        if pregunta is None:
            continue
        if respuesta is None or respuesta in pregunta["opciones"]:
            validas[pregunta_id] = respuesta
    return validas


def guardar_borrador_intento(intento_id, respuestas, ahora=None):
    """Guarda respuestas solo mientras el intento siga dentro del tiempo."""
    iniciar_base_datos()
    ahora = _como_utc(ahora)
    with conectar() as conexion:
        conexion.execute("BEGIN IMMEDIATE")
        fila = _seleccionar_intento(conexion, intento_id)
        if fila is None or fila["estado"] != "en_curso":
            return False
        if ahora > datetime.fromisoformat(fila["fin"]):
            return False
        preguntas = json.loads(fila["preguntas_json"])
        guardadas = {
            int(k): v
            for k, v in json.loads(fila["respuestas_json"] or "{}").items()
        }
        guardadas.update(_respuestas_validas(preguntas, respuestas))
        conexion.execute("""
            UPDATE intentos_examen
            SET respuestas_json = ?
            WHERE id = ? AND estado = 'en_curso'
        """, (
            json.dumps(guardadas, ensure_ascii=False), intento_id
        ))
    return True


def finalizar_intento(intento_id, respuestas=None, ahora=None):
    """Finaliza y guarda calificación y respuestas en una sola transacción."""
    iniciar_base_datos()
    ahora = _como_utc(ahora)
    with conectar() as conexion:
        conexion.execute("BEGIN IMMEDIATE")
        fila = _seleccionar_intento(conexion, intento_id)
        if fila is None:
            raise ValueError("El intento no existe.")
        if fila["estado"] == "finalizado":
            return _fila_intento(fila)

        preguntas = json.loads(fila["preguntas_json"])
        guardadas = {
            int(k): v
            for k, v in json.loads(fila["respuestas_json"] or "{}").items()
        }
        fin = datetime.fromisoformat(fila["fin"])
        if ahora <= fin:
            guardadas.update(_respuestas_validas(preguntas, respuestas))

        correctas = sum(
            1
            for pregunta in preguntas
            if guardadas.get(int(pregunta["id"])) == pregunta["respuesta"]
        )
        total = len(preguntas)
        puntaje = round(correctas / total * 100) if total else 0
        fecha = ahora.isoformat()

        for pregunta in preguntas:
            pregunta_id = int(pregunta["id"])
            respuesta = guardadas.get(pregunta_id)
            conexion.execute("""
                INSERT OR IGNORE INTO respuestas_examen
                (intento_id, estudiante, universidad, tipo_examen,
                 pregunta_id, materia, tema, dificultad, respuesta,
                 correcta, uso_pista, fecha)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                intento_id, fila["estudiante"], fila["universidad"],
                fila["tipo_examen"], pregunta_id, pregunta["materia"],
                pregunta["tema"],
                pregunta.get(
                    "dificultad", pregunta.get("nivel", "No registrada")
                ),
                respuesta, int(respuesta == pregunta["respuesta"]), 0, fecha
            ))

        if (
            fila["tipo_examen"] == "Mensual"
            and fila["modalidad"] == "oficial"
        ):
            conexion.execute("""
                INSERT INTO resultados
                (estudiante, universidad, convocatoria,
                 puntaje, fecha, intento_id)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                fila["estudiante"], fila["universidad"],
                fila["convocatoria"], puntaje, fecha, intento_id
            ))
        elif fila["tipo_examen"] == "Semanal":
            conexion.execute("""
                INSERT INTO examenes_semanales
                (estudiante, universidad, puntaje,
                 correctas, total, fecha, intento_id)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                fila["estudiante"], fila["universidad"], puntaje,
                correctas, total, fecha, intento_id
            ))

        conexion.execute("""
            UPDATE intentos_examen
            SET estado = 'finalizado', finalizado_en = ?,
                puntaje = ?, correctas = ?, total = ?, respuestas_json = ?
            WHERE id = ? AND estado = 'en_curso'
        """, (
            fecha, puntaje, correctas, total,
            json.dumps(guardadas, ensure_ascii=False), intento_id
        ))
        fila_final = _seleccionar_intento(conexion, intento_id)
    return _fila_intento(fila_final)


# Funciones compatibles con los módulos y datos ya existentes.
def guardar_resultado(estudiante, universidad, puntaje):
    iniciar_base_datos()
    estudiante, universidad = _normalizar_identidad(
        estudiante, universidad
    )
    with conectar() as conexion:
        cursor = conexion.execute("""
            INSERT OR IGNORE INTO resultados
            (estudiante, universidad, convocatoria, puntaje, fecha)
            VALUES (?, ?, ?, ?, ?)
        """, (
            estudiante, universidad, obtener_mes(), int(puntaje),
            _ahora_utc().isoformat()
        ))
        return cursor.rowcount > 0


def obtener_ranking(universidad):
    iniciar_base_datos()
    with conectar() as conexion:
        return conexion.execute("""
            SELECT estudiante, puntaje
            FROM resultados
            WHERE universidad = ? COLLATE NOCASE AND convocatoria = ?
            ORDER BY puntaje DESC, fecha ASC, id ASC
        """, (universidad, obtener_mes())).fetchall()


def preparar_tabla_progreso():
    iniciar_base_datos()


def guardar_progreso(estudiante, universidad, puntos, historial, errores):
    iniciar_base_datos()
    with conectar() as conexion:
        conexion.execute("""
            INSERT INTO progreso_estudiante
            (estudiante, universidad, puntos, historial, errores)
            VALUES (?, ?, ?, ?, ?)
            ON CONFLICT(estudiante, universidad)
            DO UPDATE SET puntos = excluded.puntos,
                          historial = excluded.historial,
                          errores = excluded.errores
        """, (
            estudiante.strip(), universidad.strip(), int(puntos),
            json.dumps(historial, ensure_ascii=False),
            json.dumps(errores, ensure_ascii=False)
        ))


def cargar_progreso(estudiante, universidad):
    iniciar_base_datos()
    with conectar() as conexion:
        resultado = conexion.execute("""
            SELECT puntos, historial, errores
            FROM progreso_estudiante
            WHERE estudiante = ? COLLATE NOCASE
              AND universidad = ? COLLATE NOCASE
        """, (estudiante, universidad)).fetchone()
    if resultado is None:
        return 0, {}, {}
    puntos, historial, errores = resultado
    historial = {int(k): v for k, v in json.loads(historial).items()}
    return puntos, historial, json.loads(errores)


def preparar_tabla_examenes():
    iniciar_base_datos()


def guardar_examen_semanal(
    estudiante, universidad, puntaje, correctas, total
):
    iniciar_base_datos()
    with conectar() as conexion:
        conexion.execute("""
            INSERT INTO examenes_semanales
            (estudiante, universidad, puntaje, correctas, total, fecha)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            estudiante, universidad, int(puntaje), int(correctas),
            int(total), _ahora_utc().isoformat()
        ))


def obtener_examenes_semanales(estudiante, universidad):
    iniciar_base_datos()
    with conectar() as conexion:
        return conexion.execute("""
            SELECT fecha, puntaje, correctas, total
            FROM examenes_semanales
            WHERE estudiante = ? COLLATE NOCASE
              AND universidad = ? COLLATE NOCASE
            ORDER BY id DESC
        """, (estudiante, universidad)).fetchall()


def obtener_historial_mensual(estudiante, universidad):
    iniciar_base_datos()
    with conectar() as conexion:
        return conexion.execute("""
            SELECT convocatoria, puntaje
            FROM resultados
            WHERE estudiante = ? COLLATE NOCASE
              AND universidad = ? COLLATE NOCASE
            ORDER BY convocatoria DESC
        """, (estudiante, universidad)).fetchall()


def preparar_tabla_respuestas():
    iniciar_base_datos()


def guardar_respuestas_examen(
    estudiante,
    universidad,
    tipo_examen,
    preguntas,
    respuestas,
    intento_id=None
):
    """Compatibilidad: evita duplicados cuando se proporciona intento_id."""
    iniciar_base_datos()
    fecha = _ahora_utc().isoformat()
    with conectar() as conexion:
        for pregunta in preguntas:
            respuesta = respuestas.get(pregunta["id"])
            conexion.execute("""
                INSERT OR IGNORE INTO respuestas_examen
                (intento_id, estudiante, universidad, tipo_examen,
                 pregunta_id, materia, tema, dificultad, respuesta,
                 correcta, uso_pista, fecha)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 0, ?)
            """, (
                intento_id, estudiante, universidad, tipo_examen,
                pregunta["id"], pregunta["materia"], pregunta["tema"],
                pregunta.get(
                    "dificultad", pregunta.get("nivel", "No registrada")
                ),
                respuesta, int(respuesta == pregunta["respuesta"]), fecha
            ))


def obtener_errores_examen(estudiante, universidad):
    iniciar_base_datos()
    with conectar() as conexion:
        return conexion.execute("""
            SELECT tema, COUNT(*)
            FROM respuestas_examen
            WHERE estudiante = ? COLLATE NOCASE
              AND universidad = ? COLLATE NOCASE
              AND correcta = 0
            GROUP BY tema
            ORDER BY COUNT(*) DESC, tema
        """, (estudiante, universidad)).fetchall()


def obtener_resumen_respuestas(estudiante, universidad):
    iniciar_base_datos()
    with conectar() as conexion:
        filas = conexion.execute("""
            SELECT tema, COUNT(*) AS total,
                   SUM(correcta) AS correctas,
                   SUM(CASE WHEN correcta = 0 THEN 1 ELSE 0 END) AS errores,
                   SUM(uso_pista) AS con_pista
            FROM respuestas_examen
            WHERE estudiante = ? COLLATE NOCASE
              AND universidad = ? COLLATE NOCASE
            GROUP BY tema
            ORDER BY errores DESC, tema
        """, (estudiante, universidad)).fetchall()
    return [
        {
            "tema": tema,
            "total": total,
            "correctas": correctas or 0,
            "errores": errores or 0,
            "con_pista": con_pista or 0
        }
        for tema, total, correctas, errores, con_pista in filas
    ]
