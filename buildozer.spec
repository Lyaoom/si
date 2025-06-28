[app]
# (str) Título de la aplicación
title = YouTube Downloader

# (str) Nombre del paquete (ASCII sin mayúsculas ni espacios)
package.name = ytdownloader

# (str) Dominio del paquete — si no tienes uno, puedes usar un genérico
package.domain = org.ytdownloader

# (str) Carpeta que contiene main.py
source.dir = .

# (list) Extensiones de archivos a incluir
source.include_exts = py,png,jpg,kv,txt

# (list) Archivos a incluir explícitamente (opcional)
# source.include_patterns = assets/*,images/*.png

# (str) Versión de tu app (puedes definir __version__ en main.py)
version = 0.1

# (str) Archivo principal
source.main = main.py

[buildozer]
# Puedes dejar vacíos los paths para usar los valores por defecto
# p4a.source_dir = ../python-for-android

[android]
android.api = 30
android.minapi = 21
android.sdk = 30
android.ndk = 25b
android.ndk_api = 21

# Permisos necesarios
android.permissions = INTERNET,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE

# Módulos que necesitas para tu app
android.requirements = python3,kivy,yt_dlp,ffmpeg

# Orientación de la pantalla
orientation = portrait

[buildozer.log]
level = 1
