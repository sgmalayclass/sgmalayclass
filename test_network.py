#!/usr/bin/env python3
import urllib.request
import os

try:
    print("🔄 Testing network IP access (192.168.1.170:8000)...")
    urllib.request.urlretrieve('http://192.168.1.170:8000/maya_chatbot_melayu_v1.0.0.apk', 'test_network.apk')
    size = os.path.getsize('test_network.apk')
    print(f"✅ Downloaded: {size} bytes")
    os.remove('test_network.apk')
    print("✅ Network IP test successful!")
    print("🎯 Your phone should be able to access this URL!")
except Exception as e:
    print(f"❌ Network test failed: {e}")
    print("💡 Make sure the server is running and firewall allows access") 