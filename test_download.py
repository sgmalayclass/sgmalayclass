#!/usr/bin/env python3
import urllib.request
import os

try:
    print("🔄 Testing APK download from localhost:8000...")
    urllib.request.urlretrieve('http://localhost:8000/maya_chatbot_melayu_v1.0.0.apk', 'test_download.apk')
    size = os.path.getsize('test_download.apk')
    print(f"✅ Downloaded: {size} bytes")
    os.remove('test_download.apk')
    print("✅ APK download test successful!")
except Exception as e:
    print(f"❌ Download test failed: {e}") 