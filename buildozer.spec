[app]
title = YouTubeDownloader
package.name = ytdownloader
package.domain = org.test
version = 0.1
source.main = main.py
source.include_exts = py,png,jpg,kv,txt

[buildozer]
android.api = 30
android.minapi = 21
android.ndk = 25b
android.sdk = 30

[android]
permissions = INTERNET, WRITE_EXTERNAL_STORAGE, READ_EXTERNAL_STORAGE
orientation = portrait
requirement = python3,kivy,yt_dlp,ffmpeg

[buildozer.log]
level = 1

