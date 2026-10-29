# PostulaMente AI

Prototipo universitario de aprendizaje adaptativo y preparación matemática.
La aplicación usa Streamlit y SQLite y conserva el progreso por estudiante y
universidad.

## Ejecutar

En Windows, abre `Iniciar_PostulaMente.bat`. También puedes ejecutar desde
PowerShell, en esta carpeta:

```powershell
.\.venv\Scripts\python.exe -m streamlit run app.py
```

La aplicación se abre en `http://localhost:8501`.

En un equipo nuevo, ejecuta primero `Instalar_PostulaMente.bat`.

## Modo demostración

En la pantalla de bienvenida, pulsa **Entrar al modo demostración**. Se cargan
datos completamente ficticios para mostrar:

- progreso y puntos;
- respuestas con y sin pistas;
- errores de procedimiento;
- dos exámenes semanales;
- tutor adaptativo;
- competidores ficticios en el ranking mensual.

Desde el menú lateral puedes pulsar **Restablecer demostración** para regresar
al estado inicial. Este proceso no elimina perfiles reales.

## Pruebas

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

Las pruebas usan bases SQLite temporales. No modifican `datos/postulamente.db`.

## Flujo recomendado para la exposición

1. Iniciar sesión con un perfil de demostración.
2. Resolver una práctica, usar una pista y mostrar cómo cambia el diagnóstico.
3. Entregar un examen semanal y revisar las respuestas guardadas.
4. Abrir el Tutor inteligente para mostrar evidencias, diagnóstico y refuerzo.
5. Realizar primero un simulacro de práctica.
6. Explicar la diferencia con el intento oficial único y abrir el ranking.
7. Mostrar Mi progreso y aclarar que el dominio es una estimación provisional.

## Persistencia e integridad

- Cada examen o simulacro tiene un identificador UUID.
- El borrador de respuestas se guarda durante el intento.
- La calificación y las respuestas se confirman en una sola transacción.
- Las respuestas posteriores al límite no se aceptan.
- Solo existe un simulacro oficial por estudiante, universidad y convocatoria.
- Los simulacros de práctica no participan en el ranking.
- Los datos antiguos se conservan y se vinculan a intentos heredados.

Las copias previas a la migración se encuentran en `datos/backups/`.

La base local, sus archivos temporales y los respaldos están excluidos del
repositorio mediante `.gitignore`.

## Publicación

Consulta `DESPLIEGUE.md` para publicar en Streamlit Community Cloud y preparar
una copia de respaldo para una computadora Windows.

## Alcance del tutor

El tutor actual es un sistema basado en reglas transparentes. Combina prácticas,
exámenes y simulacros para distinguir falta de conocimiento, errores de
procedimiento, resolución con pistas y dominio sin ayuda. No se presenta como un
modelo de aprendizaje automático entrenado ni como una probabilidad real de
ingreso universitario.
