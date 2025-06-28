#!/bin/bash

# Script para compilar APK de YouTube Downloader
# Asegúrate de tener todo instalado antes de ejecutar

echo "🚀 Iniciando proceso de compilación APK..."

# Verificar si buildozer está instalado
if ! command -v buildozer &> /dev/null; then
    echo "❌ Buildozer no está instalado. Instalando..."
    pip install buildozer
fi

# Verificar si Cython está instalado (necesario para compilar)
if ! python -c "import Cython" &> /dev/null; then
    echo "❌ Cython no está instalado. Instalando..."
    pip install Cython
fi

echo "📋 Verificando archivos necesarios..."

# Verificar que existan los archivos necesarios
if [ ! -f "main.py" ]; then
    echo "❌ Error: main.py no encontrado"
    exit 1
fi

if [ ! -f "buildozer.spec" ]; then
    echo "❌ Error: buildozer.spec no encontrado"
    exit 1
fi

echo "✅ Archivos encontrados"

# Limpiar compilaciones anteriores
echo "🧹 Limpiando compilaciones anteriores..."
buildozer android clean

# Inicializar buildozer (primera vez)
echo "🔧 Inicializando buildozer..."
buildozer init

# Compilar APK en modo debug
echo "🔨 Compilando APK (esto puede tardar mucho la primera vez)..."
buildozer android debug

# Verificar si la compilación fue exitosa
if [ -f "./bin/youtubedownloader-1.0-arm64-v8a-debug.apk" ] || [ -f "./bin/youtubedownloader-1.0-armeabi-v7a-debug.apk" ]; then
    echo "🎉 ¡APK compilado exitosamente!"
    echo "📱 El archivo APK está en la carpeta './bin/'"
    ls -la ./bin/*.apk
else
    echo "❌ Error en la compilación. Revisa los logs arriba."
    exit 1
fi

echo "📝 Instrucciones:"
echo "1. Transfiere el archivo APK a tu teléfono Android"
echo "2. Habilita 'Orígenes desconocidos' en configuración"
echo "3. Instala el APK"
echo "4. ¡Disfruta tu app!"