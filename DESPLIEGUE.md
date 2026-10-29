# Despliegue y presentación de PostulaMente AI

## Estrategia recomendada

La exposición debe tener dos rutas disponibles:

1. **Principal:** aplicación publicada en Streamlit Community Cloud.
2. **Respaldo:** aplicación local iniciada con `Iniciar_PostulaMente.bat`.

La base SQLite de la versión publicada es temporal. El botón **Entrar al modo
demostración** crea datos ficticios cada vez que la instancia necesita comenzar
desde cero. La base real del equipo y sus respaldos están excluidos de Git.

## Publicación en Streamlit Community Cloud

1. Subir este proyecto a un repositorio de GitHub.
2. Abrir <https://share.streamlit.io>.
3. Elegir **Create app** y seleccionar el repositorio.
4. Elegir la rama `main` y el archivo `app.py`.
5. En configuración avanzada, seleccionar Python 3.12.
6. Publicar y esperar a que el estado indique que la aplicación está activa.
7. Abrir el enlace desde una ventana privada y probar el modo demostración.

No es necesario configurar secretos para esta versión.

## Instalación en otra computadora Windows

1. Copiar la carpeta o descomprimir el paquete portátil.
2. Instalar Python 3.12 si el equipo no lo tiene.
3. Ejecutar `Instalar_PostulaMente.bat` una vez.
4. Ejecutar `Iniciar_PostulaMente.bat`.
5. Abrir `http://localhost:8501` si el navegador no se abre automáticamente.

La instalación inicial requiere internet para descargar Streamlit y Pandas.

## Lista de respaldo para la universidad

- Laptop cargada y cargador.
- Enlace de Streamlit guardado y código QR.
- Paquete portátil en una memoria USB.
- Copia de la base de demostración.
- Video corto y capturas de las pantallas principales.
- Presentación en PDF o PowerPoint.

## Datos y privacidad

- No subir `datos/postulamente.db`.
- No subir `datos/backups/`.
- Usar nombres ficticios durante la exposición.
- Restablecer el modo demostración antes de comenzar.
- No presentar el indicador de dominio como probabilidad real de ingreso.
