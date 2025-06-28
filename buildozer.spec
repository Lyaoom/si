[app]
# (str) Title of your application
title = YouTube Downloader
# (str) Package name
package.name = ytdownloader
# (str) Package domain (needed for android/ios packaging)
package.domain = org.example
# (str) Source code where the main.py live
# Assuming you clone the GitHub repo into the project root
source.dir = .
# (str) Application versioning (method 1)
version = 1.0.0

# (list) Application requirements
# Kivy and threading are part of Python stdlib; include yt-dlp as external
requirements = python3,kivy,yt-dlp

# (str) Supported orientation (one of landscape, portrait or all)
orientation = portrait

# (bool) Include source code in the APK
#android.include_source = False

[buildozer]
# Force build to continue even if a requirement fails to install
# (useful to compile even with code errors)
requirement_fail_on_install_error = False

# (str) Path to buildozer executable if not on PATH
#buildozer = /usr/local/bin/buildozer

# (str) Log level (0 = error only, 1 = info, 2 = debug)
log_level = 1

# (int) Display warning if buildozer.spec is changed since last run
warn_on_root = 1

# Android specific

# (int) Android API to use
android.api = 31
# (int) Minimum API your APK will support
android.minapi = 21
# (int) Android SDK version to use for build
android.sdk = 20

# Permissions
android.permissions = INTERNET, WRITE_EXTERNAL_STORAGE, READ_EXTERNAL_STORAGE

# (str) Android entry point, default is ok
#android.entrypoint = org.kivy.android.PythonActivity

# (bool) Android private storage (default True)
android.private_storage = True

