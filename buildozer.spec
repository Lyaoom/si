[app]

# (str) Título de tu aplicación
title = YouTube Downloader

# (str) Nombre del paquete
package.name = youtubedownloader

# (str) Dominio del paquete (usado para el ID de Android)
package.domain = org.example

# (str) Archivo fuente principal de tu aplicación
source.main = main.py

# (list) Directorio fuente donde vive la aplicación
source.dir = .

# (list) Patrones de archivos a incluir (por defecto: *)
source.include_exts = py,png,jpg,kv,atlas

# (str) Versión de la aplicación
version = 1.0

# (list) Requerimientos de la aplicación
# Aquí incluyes todas las librerías que necesitas
requirements = python3,kivy,yt-dlp,pycryptodome,websockets,brotli,certifi,urllib3,mutagen,ffmpeg-python

# (str) Icono de la aplicación (opcional)
#icon.filename = %(source.dir)s/icon.png

# (str) Presplash de la aplicación (opcional)
#presplash.filename = %(source.dir)s/presplash.png

[buildozer]

# (int) Nivel de log (0 = solo errores, 1 = info, 2 = debug)
log_level = 2

# (int) Mostrar warnings de buildozer
warn_on_root = 1

[android]

# (bool) Habilitar AndroidX
enable_androidx = True

# (list) Permisos de Android
android.permissions = INTERNET,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE

# (str) NDK API que se usará
android.ndk_api = 21

# (str) API mínima para que funcione tu app
android.minapi = 21

# (str) API de destino de Android, debería ser tan alta como sea posible
android.api = 33

# (str) Versión del NDK de Android
android.ndk = 25b

# (str) Versión del SDK de Android
android.sdk = 33

# (bool) Usar --private data storage (True) o --dir public storage (False)
android.private_storage = True

# (str) Orientación (landscape, portrait o all)
orientation = portrait

# (bool) Indicar si la aplicación debería estar en pantalla completa o no
fullscreen = 0

# (str) Splash screen
android.presplash_color = #FFFFFF

# (str) Gradle dependencies
android.gradle_dependencies = 

# (str) Java build tool
android.gradle_tool = gradle

[buildozer:docker]
# Si quieres usar Docker para compilar (recomendado para principiantes)
# docker_build = 1