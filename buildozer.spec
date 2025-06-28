[app]

title = MiApp
package.name = miapp
package.domain = com.esteban.miapp
version = 1.0.0

# Ruta del código fuente
source.dir = .
source.main = main.py
source.include_exts = py,png,jpg,kv,atlas,mp4,txt,json

orientation = portrait

# requirements necesarios
requirements = python3,kivy,yt_dlp

# Android SDK/NDK config
android.minapi = 21
android.api = 33
android.ndk = 23b
android.ndk_api = 21

android.use_androidx = True
android.debug = True

# Permisos para almacenamiento y segundo plano
android.permissions = INTERNET,READ_EXTERNAL_STORAGE,WRITE_EXTERNAL_STORAGE,FOREGROUND_SERVICE,WAKE_LOCK,RECEIVE_BOOT_COMPLETED
android.managed_storage = true

# Arquitectura (opcional)
# android.archs = armeabi-v7a, arm64-v8a

# Carpeta de salida
build_dir = ./.buildozer
bin_dir = ./bin

# Pantalla completa
fullscreen = 0


[buildozer]

log_level = 2
logcat_on_launch = 1
warn_on_root = 1
