[app]

# Uygulama bilgileri
title = Stok Takip Sistemi
package.name = stoktakip
package.domain = com.osman

# Kaynak dosyalar
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,db

# sadece bir kez

# Sürüm
version = 1.0

# Gerekli paketler (EN ÖNEMLİ SATIR!)
requirements = python3,kivy==2.3.0,kivymd==1.2.0,sqlite3,pyjnius

# Ekran yönü
orientation = portrait
fullscreen = 0

# Android izinleri
android.permissions = WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE

# Android hedefleri
android.api = 33
android.minapi = 21
android.ndk = 25b
android.archs = armeabi-v7a, arm64-v8a

[buildozer]
log_level = 2
warn_on_root = 1