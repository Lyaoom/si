@echo off
echo 🚀 Iniciando proceso de compilacion APK...

REM Verificar si buildozer está instalado
python -c "import buildozer" 2>nul
if %errorlevel% neq 0 (
    echo ❌ Buildozer no está instalado. Instalando...
    pip install buildozer
)

REM Verificar si Cython está instalado
python -c "import Cython" 2>nul
if %errorlevel% neq 0 (
    echo ❌ Cython no está instalado. Instalando...
    pip install Cython
)

echo 📋 Verificando archivos necesarios...

REM Verificar archivos necesarios
if not exist "main.py" (
    echo ❌ Error: main.py no encontrado
    pause
    exit /b 1
)

if not exist "buildozer.spec" (
    echo ❌ Error: buildozer.spec no encontrado
    pause
    exit /b 1
)

echo ✅ Archivos encontrados

echo 🧹 Limpiando compilaciones anteriores...
buildozer android clean

echo 🔧 Inicializando buildozer...
buildozer init

echo 🔨 Compilando APK (esto puede tardar mucho la primera vez)...
buildozer android debug

REM Verificar si la compilación fue exitosa
if exist "bin\*.apk" (
    echo 🎉 ¡APK compilado exitosamente!
    echo 📱 El archivo APK está en la carpeta 'bin\'
    dir bin\*.apk
) else (
    echo ❌ Error en la compilación. Revisa los logs arriba.
    pause
    exit /b 1
)

echo.
echo 📝 Instrucciones:
echo 1. Transfiere el archivo APK a tu teléfono Android
echo 2. Habilita 'Orígenes desconocidos' en configuración
echo 3. Instala el APK
echo 4. ¡Disfruta tu app!
pause