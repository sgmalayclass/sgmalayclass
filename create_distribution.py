#!/usr/bin/env python3
"""
Create Distribution Package for Maya Chatbot
Generates QR codes, HTML pages, and complete distribution system
"""

from apk_distribution_system import APKDistributionSystem
import os
from pathlib import Path

def main():
    print("📦 Creating Maya Chatbot Distribution Package...")
    print("=" * 50)
    
    # Initialize distribution system
    distributor = APKDistributionSystem("https://maya-chatbot.github.io")
    
    # Check if APK exists
    apk_path = "bin/malaychatbot-1.0-debug.apk"
    if not Path(apk_path).exists():
        print(f"⚠️  APK not found at {apk_path}")
        print("📝 Creating placeholder for testing...")
        Path("bin").mkdir(exist_ok=True)
        with open(apk_path, "w") as f:
            f.write("# Placeholder APK for distribution testing\n")
    
    try:
        # Create complete distribution package
        package = distributor.create_complete_distribution_package(
            app_name="Maya Chatbot Melayu",
            apk_path=apk_path,
            version="1.0.0",
            description="Maya is a friendly Malay chatbot designed to help you practice conversational Bahasa Melayu with Singapore context. Features include greetings, food ordering, family conversations, and cultural references specific to Singapore."
        )
        
        print("✅ Distribution package created successfully!")
        print(f"📱 APK: {package['apk_info']['filename']}")
        print(f"📋 HTML Page: {package['html_page']}")
        print(f"🔗 Distribution URL: {package['distribution_url']}")
        print("\n📱 QR Codes generated:")
        for qr_type, qr_path in package['qr_codes'].items():
            print(f"  📱 {qr_type.title()}: {qr_path}")
        
        # Create sharing instructions
        print("\n" + "=" * 50)
        print("📤 SHARING INSTRUCTIONS")
        print("=" * 50)
        print("1. QR Codes created in: qr_codes/ folder")
        print("2. HTML download page: ready for web hosting")
        print("3. Share QR codes via:")
        print("   - WhatsApp/Telegram")
        print("   - Social media posts")
        print("   - Email attachments")
        print("   - Print for physical distribution")
        print("4. Users scan QR → Download APK → Install → Use!")
        
        return True
        
    except Exception as e:
        print(f"❌ Error creating distribution package: {e}")
        return False

if __name__ == "__main__":
    success = main()
    if success:
        print("\n🎉 Maya Chatbot distribution package ready!")
    else:
        print("\n❌ Distribution package creation failed") 