#!/usr/bin/env python3
"""
Maya Chatbot Deployment Status Checker
Shows current status of APK build and distribution system
"""

import os
from pathlib import Path
import json
import subprocess

def check_build_status():
    """Check if APK build is complete"""
    print("🔨 APK Build Status:")
    print("-" * 30)
    
    # Check for buildozer directory
    buildozer_dir = Path(".buildozer")
    if buildozer_dir.exists():
        print("✅ Buildozer initialized")
    else:
        print("⚠️  Buildozer not initialized")
    
    # Check for APK in bin directory
    bin_dir = Path("bin")
    if bin_dir.exists():
        apk_files = list(bin_dir.glob("*.apk"))
        if apk_files:
            for apk in apk_files:
                size_mb = apk.stat().st_size / (1024 * 1024)
                if size_mb > 10:  # Real APK should be > 10MB
                    print(f"✅ APK ready: {apk.name} ({size_mb:.1f} MB)")
                else:
                    print(f"⚠️  APK placeholder: {apk.name} ({size_mb:.1f} MB)")
        else:
            print("⚠️  No APK files found")
    else:
        print("❌ Bin directory not found")

def check_distribution_status():
    """Check distribution system status"""
    print("\n📦 Distribution System Status:")
    print("-" * 35)
    
    # Check QR codes
    qr_dir = Path("qr_codes")
    if qr_dir.exists():
        qr_files = list(qr_dir.glob("*.png"))
        html_files = list(qr_dir.glob("*.html"))
        
        print(f"✅ QR codes: {len(qr_files)} generated")
        for qr in qr_files:
            print(f"  📱 {qr.name}")
        
        print(f"✅ HTML pages: {len(html_files)} created")
        for html in html_files:
            print(f"  📄 {html.name}")
    else:
        print("❌ QR codes directory not found")
    
    # Check APK releases
    releases_dir = Path("apk_releases")
    if releases_dir.exists():
        apk_files = list(releases_dir.glob("*.apk"))
        print(f"✅ APK releases: {len(apk_files)} ready")
        for apk in apk_files:
            size_mb = apk.stat().st_size / (1024 * 1024)
            print(f"  📱 {apk.name} ({size_mb:.1f} MB)")
    else:
        print("⚠️  APK releases directory not found")

def check_security_status():
    """Check security implementation status"""
    print("\n🔒 Security Status:")
    print("-" * 20)
    
    security_files = [
        "security_audit_and_fixes.py",
        "security_utils.py", 
        "secure_storage.py",
        "SECURITY_REPORT.md",
        "SECURITY_SUMMARY.md"
    ]
    
    for file in security_files:
        if Path(file).exists():
            print(f"✅ {file}")
        else:
            print(f"❌ {file}")

def check_dependencies():
    """Check required dependencies"""
    print("\n📦 Dependencies Status:")
    print("-" * 25)
    
    required_packages = [
        "kivy", "buildozer", "qrcode", "pillow"
    ]
    
    for package in required_packages:
        try:
            __import__(package)
            print(f"✅ {package}")
        except ImportError:
            print(f"❌ {package} - Not installed")

def show_next_steps():
    """Show next steps based on current status"""
    print("\n🚀 Next Steps:")
    print("-" * 15)
    
    bin_dir = Path("bin")
    real_apk_exists = False
    
    if bin_dir.exists():
        for apk in bin_dir.glob("*.apk"):
            size_mb = apk.stat().st_size / (1024 * 1024)
            if size_mb > 10:
                real_apk_exists = True
                break
    
    if not real_apk_exists:
        print("1. ⏳ Wait for APK build to complete (30-60 minutes)")
        print("2. 🔄 Check build progress: buildozer android debug")
        print("3. 📱 Once APK is built, update distribution package")
    else:
        print("1. ✅ APK is ready!")
        print("2. 🌐 Start local server: python start_distribution_server.py")
        print("3. 📱 Test QR codes with your phone")
        print("4. 📤 Share QR codes with users")
        print("5. 🚀 Deploy to GitHub Pages or hosting service")

def main():
    """Main status check"""
    print("🇸🇬 Maya Chatbot - Deployment Status")
    print("=" * 40)
    
    check_build_status()
    check_distribution_status()
    check_security_status()
    check_dependencies()
    show_next_steps()
    
    print("\n" + "=" * 40)
    print("📊 Status Summary:")
    
    # Quick status indicators
    bin_dir = Path("bin")
    qr_dir = Path("qr_codes") 
    security_file = Path("SECURITY_SUMMARY.md")
    
    build_ready = bin_dir.exists() and any(apk.stat().st_size > 10*1024*1024 for apk in bin_dir.glob("*.apk"))
    distribution_ready = qr_dir.exists() and len(list(qr_dir.glob("*.png"))) > 0
    security_ready = security_file.exists()
    
    print(f"🔨 APK Build: {'✅ Ready' if build_ready else '⏳ In Progress'}")
    print(f"📦 Distribution: {'✅ Ready' if distribution_ready else '⚠️ Partial'}")
    print(f"🔒 Security: {'✅ Ready' if security_ready else '❌ Missing'}")
    
    if build_ready and distribution_ready and security_ready:
        print("\n🎉 DEPLOYMENT COMPLETE! Ready to share! 🚀")
    else:
        print("\n⏳ Deployment in progress... Please wait or check issues above.")

if __name__ == "__main__":
    main() 