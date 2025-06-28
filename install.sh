#!/bin/bash

# YouTube Downloader - Script de instalación y compilación automática
# Para WSL/Ubuntu

set -e  # Salir si hay errores

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Función para mostrar mensajes
log() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

error() {
    echo -e "${RED}[ERROR]${NC} $1"
    exit 1
}

# Verificar que estamos en WSL/Linux
if [[ "$OSTYPE" != "linux-gnu"* ]]; then
    error "Este script está diseñado para WSL/Ubuntu Linux"
fi

log "🚀 Iniciando instalación completa de YouTube Downloader para Android..."

# 1. Actualizar sistema
log "📦 Actualizando sistema..."
sudo apt update && sudo apt upgrade -y

# 2. Instalar dependencias del sistema
log "🔧 Instalando dependencias del sistema..."
sudo apt install -y \
    git zip unzip curl wget \
    openjdk-17-jdk \
    python3 python3-dev python3-pip python3-venv \
    autoconf libtool pkg-config \
    zlib1g-dev libncurses5-dev libncursesw5-dev libtinfo5 \
    cmake libffi-dev libssl-dev \
    build-essential ccache m4 \
    libc6-dev libgmp-dev libmpc-dev libmpfr-dev \
    lld

# 3. Crear directorio del proyecto
PROJECT_DIR="$HOME/youtube_downloader_android"
log "📁 Creando directorio del proyecto en: $PROJECT_DIR"

if [ -d "$PROJECT_DIR" ]; then
    warn "El directorio ya existe. Eliminando..."
    rm -rf "$PROJECT_DIR"
fi

mkdir -p "$PROJECT_DIR"
cd "$PROJECT_DIR"

# 4. Clonar repositorio
log "📥 Clonando repositorio desde GitHub..."
git clone https://github.com/Lyaoom/si.git .

# 5. Crear entorno virtual
log "🐍 Creando entorno virtual de Python..."
python3 -m venv venv
source venv/bin/activate

# 6. Actualizar pip y instalar dependencias Python
log "📚 Instalando dependencias de Python..."
pip install --upgrade pip setuptools wheel

# Instalar Cython primero (crítico para buildozer)
pip install Cython==0.29.33

# Instalar buildozer y otras dependencias
pip install buildozer

# Instalar dependencias de la app
pip install \
    kivy>=2.1.0 \
    yt-dlp>=2023.7.6 \
    certifi \
    urllib3 \
    requests \
    mutagen \
    websockets \
    pycryptodomex

# 7. Configurar variables de entorno
log "⚙️ Configurando variables de entorno..."
export ANDROIDSDK="$HOME/.buildozer/android/platform/android-sdk"
export ANDROIDNDK="$HOME/.buildozer/android/platform/android-ndk-r25b"
export ANDROIDAPI="33"
export NDKAPI="21"
export ANDROIDARCH="arm64-v8a"

# Agregar al .bashrc para futuras sesiones
if ! grep -q "ANDROIDSDK" ~/.bashrc; then
    echo "" >> ~/.bashrc
    echo "# Android Build Environment" >> ~/.bashrc
    echo 'export ANDROIDSDK="$HOME/.buildozer/android/platform/android-sdk"' >> ~/.bashrc
    echo 'export ANDROIDNDK="$HOME/.buildozer/android/platform/android-ndk-r25b"' >> ~/.bashrc
    echo 'export ANDROIDAPI="33"' >> ~/.bashrc
    echo 'export NDKAPI="21"' >> ~/.bashrc
    echo 'export ANDROIDARCH="arm64-v8a"' >> ~/.bashrc
fi

# 8. Crear/actualizar buildozer.spec optimizado
log "📝 Creando configuración de buildozer..."
cat > buildozer.spec << 'EOF'
[app]

# (str) Title of your application
title = YouTube Downloader

# (str) Package name
package.name = youtubedownloader

# (str) Package domain (needed for android/ios packaging)
package.domain = org.lyaoom

# (str) Source code where the main.py live
source.dir = .

# (list) Source files to include (let empty to include all the files)
source.include_exts = py,png,jpg,kv,atlas,txt

# (str) Application versioning (method 1)
version = 1.0

# (list) Application requirements
# Note: yt-dlp incluye ffmpeg automáticamente
requirements = python3,kivy,pyjnius,android,yt-dlp,certifi,urllib3,requests,mutagen,websockets,pycryptodomex

# (str) Supported orientation (landscape, portrait or all)
orientation = portrait

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 0

# (list) Permissions
android.permissions = android.permission.INTERNET,android.permission.WRITE_EXTERNAL_STORAGE,android.permission.READ_EXTERNAL_STORAGE,android.permission.WAKE_LOCK,android.permission.ACCESS_NETWORK_STATE,android.permission.MANAGE_EXTERNAL_STORAGE

# (str) Android NDK version to use
android.ndk = 25b

# (str) Android SDK version to use
android.sdk = 33

# (str) Android NDK API to use
android.ndk_api = 21

# (str) Android SDK API to use
android.api = 33

# (str) Android arch to build for
android.archs = arm64-v8a

# (str) Android entry point
android.entrypoint = org.kivy.android.PythonActivity

# (str) Android app theme
android.theme = @android:style/Theme.NoTitleBar

# (bool) Enable AndroidX support
android.enable_androidx = True

# (str) Android logcat filters to use
android.logcat_filters = *:S python:D

# (bool) Enable Android auto backup feature
android.allow_backup = True

# (bool) Copy library instead of making a libpymodules.so
android.copy_libs = 1

# (str) The format used to package the app for release mode
android.release_artifact = apk

# (str) The format used to package the app for debug mode
android.debug_artifact = apk

# (bool) Use --private data storage (True) or --dir public storage (False)
android.private_storage = True

# (str) Gradle dependencies
android.gradle_dependencies = 

# (list) Gradle repositories
android.gradle_repositories = 

# (str) Bootstrap to use for android builds
android.bootstrap = sdl2

# (int) Target Android API, should be as high as possible
android.minapi = 21

[buildozer]

# (int
