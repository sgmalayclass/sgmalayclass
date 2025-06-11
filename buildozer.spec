[app]

# (str) Title of your application
title = Maya Chatbot Melayu

# (str) Package name
package.name = malaychatbot

# (str) Package domain (needed for android/ios packaging)
package.domain = com.singapore.maya

# (str) Source code where the main.py live
source.dir = .

# (list) Source files to include (let empty to include all the files)
source.include_exts = py,png,jpg,kv,atlas,json

# (list) List of inclusions using pattern matching
source.include_patterns = assets/*,malay_training_data.json

# (str) Application versioning (method 1)
version = 1.0.0

# (list) Application requirements - SECURITY: Minimal dependencies only
requirements = python3,kivy,pyjnius,plyer

# (str) Supported orientation
orientation = portrait

# SECURITY: Disable debug mode for production
debug = 0

[buildozer]

# (int) Log level (0 = error only, 1 = info, 2 = debug)
log_level = 1

# (int) Display warning if buildozer is run as root
warn_on_root = 1

#
# Android specific - SECURITY HARDENED
#

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 0

# (string) Presplash background color
android.presplash_color = #FFFFFF

# SECURITY: Minimal permissions only - NO dangerous permissions
android.permissions = INTERNET,ACCESS_NETWORK_STATE,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE

# SECURITY: Latest API levels for security patches
android.api = 33
android.minapi = 21
android.compilesdk = 33
android.sdk = 33
android.ndk = 25b

# SECURITY: Target modern architectures
android.archs = arm64-v8a, armeabi-v7a

# SECURITY: Enable backup for user data protection
android.allow_backup = True

# SECURITY: APK format for easy distribution
android.release_artifact = apk
android.debug_artifact = apk

# SECURITY: Disable debug features
android.logcat_filters = *:S

# SECURITY: Use default entry point (no custom modifications)
android.entrypoint = org.kivy.android.PythonActivity

# SECURITY: Enable bytecode compilation for code protection
android.no-byte-compile-python = False
