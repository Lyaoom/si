[app]

# (str) Title of your application
title = YouTube Downloader

# (str) Package name
package.name = youtubedownloader

# (str) Package domain (needed for android/ios packaging)
package.domain = com.lyaoom.youtubedownloader

# (str) Source code where the main.py live
source.dir = .

# (list) Source files to include (let empty to include all the files)
source.include_exts = py,png,jpg,kv,atlas,txt

# (str) Application versioning (method 1)
version = 1.0

# (list) Application requirements
requirements = python3,kivy,kivymd,pyjnius,plyer,yt-dlp,certifi,urllib3,requests,websockets,mutagen,pycryptodomex,brotli

# (str) Presplash of the application
#presplash.filename = %(source.dir)s/presplash.png

# (str) Icon of the application
#icon.filename = %(source.dir)s/icon.png

# (str) Supported orientation (landscape, sensorLandscape, portrait, sensorPortrait or all)
orientation = portrait

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 0

[buildozer]

# (int) Log level (0 = error only, 1 = info, 2 = debug (with command output))
log_level = 2

# (int) Display warning if buildozer is run as root (0 = False, 1 = True)
warn_on_root = 1

[android]

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 0

# (list) Permissions
android.permissions = INTERNET,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE

# (int) Target Android API, should be as high as possible.
android.api = 34

# (int) Minimum API your APK / AAB will support.
android.minapi = 21

# (str) Android NDK version to use
android.ndk = 25c

# (str) Android SDK version to use
android.sdk = 34

# (bool) Use --private data storage (True) or --dir public storage (False)
android.private_storage = False

# (str) Android arch to build for, choices: armeabi-v7a, arm64-v8a, x86, x86_64
android.archs = arm64-v8a, armeabi-v7a

# (bool) enables Android auto backup feature (Android API >=23)
android.allow_backup = True

# (str) The format used to package the app for release mode (aab or apk).
android.release_artifact = apk

# (str) The format used to package the app for debug mode (apk or aab).
android.debug_artifact = apk

[buildozer]
# Logs are stored in .buildozer/logs/
log_level = 2
