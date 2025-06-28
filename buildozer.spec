[app]

# (str) Title of your application
title = YouTube Downloader

# (str) Package name
package.name = youtubedownloader

# (str) Package domain (needed for android/ios packaging)
package.domain = org.example

# (str) Source code where the main.py live
source.dir = .

# (list) Source files to include (let empty to include all the files)
source.include_exts = py,png,jpg,kv,atlas

# (str) Application versioning (method 1)
version = 1.0

# (list) Application requirements
requirements = python3,kivy,pyjnius,android,yt-dlp,certifi,urllib3,requests,mutagen,websockets,pycryptodomex

# (str) Supported orientation (landscape, portrait or all)
orientation = portrait

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 0

# (list) Permissions
android.permissions = android.permission.INTERNET,android.permission.WRITE_EXTERNAL_STORAGE,android.permission.READ_EXTERNAL_STORAGE,android.permission.WAKE_LOCK,android.permission.ACCESS_NETWORK_STATE

# (str) Android NDK version to use
android.ndk = 25b

# (str) Android SDK version to use
android.sdk = 33

# (str) ANT directory (auto-detected if empty)
android.ant_path = 

# (str) Android NDK directory (auto-detected if empty)
android.ndk_path = 

# (str) Android SDK directory (auto-detected if empty)
android.sdk_path = 

# (str) Android entry point, default is ok for Kivy-based app
android.entrypoint = org.kivy.android.PythonActivity

# (str) Full name including package path of the Java class that implements Python Service
android.service = 

# (str) Android app theme, default is ok for Kivy-based app
android.theme = @android:style/Theme.NoTitleBar

# (list) Pattern to whitelist for the whole project
android.whitelist = 

# (bool) Enable AndroidX support. Enable when 'android.gradle_dependencies'
# contains an 'androidx' package, or any package from Kotlin source.
android.enable_androidx = True

# (str) Android logcat filters to use
android.logcat_filters = *:S python:D

# (bool) Enable Android auto backup feature (Android API >=23)
android.allow_backup = True

# (str) XML file for Android auto backup rules
android.backup_rules = 

# (bool) Copy library instead of making a libpymodules.so
android.copy_libs = 1

# (str) The format used to package the app for release mode (aab or apk).
android.release_artifact = apk

# (str) The format used to package the app for debug mode (apk).
android.debug_artifact = apk

[buildozer]

# (int) Log level (0 = error only, 1 = info, 2 = debug (with command output))
log_level = 2

# (int) Display warning if buildozer is run as root (0 = False, 1 = True)
warn_on_root = 1

# (str) Path to build artifact storage, absolute or relative to spec file
build_dir = ./.buildozer

# (str) Path to build output (i.e. .apk, .aab, .ipa) storage
bin_dir = ./bin
