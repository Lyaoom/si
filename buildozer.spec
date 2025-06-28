[app]

# (str) Título de tu aplicación.
title = Mi Aplicacion Si

# (str) Nombre del paquete. Debe ser único, minúsculas, sin espacios ni caracteres especiales.
package.name = com.lyaoom.si_app

# (str) Dominio del paquete (necesario para empaquetado Android/iOS).
# Generalmente, es el dominio de tu organización o el tuyo propio, invertido.
package.domain = org.lyaoom

# (str) Versión de la aplicación.
version = 0.1

# (list) Requisitos de Python. ESTO ES CRÍTICO.
# Enumera todas las bibliotecas de Python que tu aplicación necesita, separadas por comas.
# Si tu app usa Kivy, Pygame, etc., inclúyelos. Si no usas ninguna GUI, 'python3' puede ser suficiente.
# EJEMPLOS:
# requirements = python3,kivy
# requirements = python3,requests,numpy
# requirements = python3,pygame
requirements = python3,kivy

# (str) El directorio que contiene el código fuente de tu aplicación.
# Por defecto es el directorio actual donde se ejecuta buildozer.
source.dir = .

# (str) El archivo principal de tu aplicación (el punto de entrada).
# Asegúrate de que este archivo exista en la raíz de tu 'source.dir'.
main.py = main.py

# (str) Orientación por defecto de tu aplicación: landscape, portrait, all.
orientation = portrait

# (bool) Si la aplicación se ejecutará en pantalla completa (0 = no, 1 = sí).
fullscreen = 0

# (list) Permisos de Android que tu aplicación necesita.
# Siempre es buena práctica incluir INTERNET si la app se conecta a la red.
# Si tu app necesita acceder al almacenamiento, red, cámara, etc., añádelos aquí.
# android.permissions = INTERNET, READ_EXTERNAL_STORAGE, WRITE_EXTERNAL_STORAGE, CAMERA
android.permissions = INTERNET

# (str) El nivel de API de Android objetivo para compilar.
# Se recomienda usar una versión reciente y compatible. Puedes probar con 31, 32 o 33.
android.api = 33

# (int) El nivel de API mínimo de Android que tu aplicación soportará.
# Manténlo razonablemente bajo para compatibilidad, pero no tan bajo que falten funciones.
android.minapi = 21

# (int) El nivel de API de Android con el que se compila la aplicación.
# Suele ser el mismo que android.api o superior.
android.targetsdk = 33

# (str) La categoría de la aplicación (opcional, para tiendas de apps).
# android.category = productivity

# (list) Opciones para el Android Manifest.
# android.extra_manifest_xml = <uses-feature android:name="android.hardware.usb.host" android:required="true" />

[buildozer]

# (list) Arquitecturas Android a las que apuntar.
# 'armeabi-v7a' para dispositivos de 32 bits, 'arm64-v8a' para 64 bits.
# Es buena práctica incluir ambas para máxima compatibilidad.
android.archs = arm64-v8a, armeabi-v7a

# (int) Número de procesos a usar para la compilación.
# jobs = 1

# (bool) Habilitar el modo de depuración. Genera un APK debuggeable.
debug = True

# (bool) Si es para lanzamiento (release = True) se necesita firmar el APK y otras configuraciones.
# Para desarrollo y pruebas, déjalo en False.
release = False

# (str) Ruta a tu archivo keystore si estás construyendo una versión de lanzamiento.
# android.release_keystore = ~/my-release-key.keystore

# (str) Alias de la clave dentro del keystore.
# android.release_keystore_alias = my_app_alias

# (str) Contraseña para el keystore (sólo si se usa release_keystore).
# android.release_keystore_pass = your_password

# (str) Contraseña para el alias (sólo si se usa release_keystore).
# android.release_keyalias_pass = your_password

# (bool) Si se deben limpiar los directorios de compilación y las herramientas antes de compilar.
# android.clean_build = True

# (bool) Si Buildozer debe usar una caché para las dependencias (más rápido en compilaciones sucesivas).
# android.use_setup_py = True

# (bool) Incluir o no los libs locales. Si tu proyecto tiene módulos locales, déjalo en True.
# android.add_local_libs = True
