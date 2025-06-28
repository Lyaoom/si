[app]

# Nombre de la aplicación
title = MiApp

# Nombre interno del paquete
package.name = miapp

# Dominio inverso para identificar la app (puedes personalizarlo)
package.domain = com.esteban.miapp

# Versión de la app
version = 1.0.0

# Archivo principal
source.main = main.py

# Extensiones de archivos incluidas
source.include_exts = py,png,jpg,kv,atlas,mp4,txt,json

# Orientación de la pantalla
orientation = portrait

# Icono (puedes reemplazar con tu propio icono PNG)
# icon.filename = %(source.dir)s/icon.png

# Requisitos de Python
requirements = python3,kivy,yt_dlp

# Motor de entrada (opcional)
# input.providers = keyboard

# SDKs de Android
android.minapi = 21
android.api = 33
android.ndk = 23b
android.ndk_api = 21

# Usa AndroidX (recomendado)
android.use_androidx = True

# Permisos necesarios para archivos y segundo plano
android.permissions = INTERNET,READ_EXTERNAL_STORAGE,WRITE_EXTERNAL_STORAGE,FOREGROUND_SERVICE,WAKE_LOCK,RECEIVE_BOOT_COMPLETED

# Soporte para almacenamiento gestionado (Android 11+)
android.managed_storage = true

# Desactiva log del compilador (opcional)
# android.logcat_filters = *:S python:D

# Archivos ocultos a excluir
# source.exclude_dirs = tests, bin, .git, .vscode

# Limita la arquitectura si deseas reducir tamaño
# android.archs = arm64-v8a

# Ejecutar en modo debug
android.debug = True

# Directorios de compilación
build_dir = ./.buildozer
bin_dir = ./bin

# Modo fullscreen
fullscreen = 0


[buildozer]

# Archivos a incluir en dist/
# include_patterns = assets/*,images/*.png

# Directorio para guardar compilaciones
log_level = 2

# Correr logcat después de ejecutar
logcat_on_launch = 1

# Reintentar builds fallidos automáticamente
warn_on_root = 6
