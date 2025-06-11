#!/usr/bin/env python3
"""
Create Local QR Codes for Maya Chatbot
Generates QR codes pointing to localhost:8000 for immediate testing
"""

import qrcode
from pathlib import Path

def create_local_qr_codes():
    """Create QR codes pointing to local server"""
    print("📱 Creating Local QR Codes for Maya Chatbot...")
    print("=" * 50)
    
    # Local server URLs
    base_url = "http://localhost:8000"
    download_url = f"{base_url}/maya_chatbot_melayu_v1.0.0.apk"
    page_url = f"{base_url}/maya_chatbot_melayu_download.html"
    
    qr_codes = {
        "download": {
            "url": download_url,
            "filename": "maya_chatbot_LOCAL_download_qr.png",
            "description": "Direct APK Download"
        },
        "page": {
            "url": page_url, 
            "filename": "maya_chatbot_LOCAL_page_qr.png",
            "description": "Download Page"
        }
    }
    
    # Create QR codes directory
    qr_dir = Path("qr_codes")
    qr_dir.mkdir(exist_ok=True)
    
    for qr_type, info in qr_codes.items():
        print(f"🔗 Creating {qr_type} QR code...")
        
        # Create QR code
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(info["url"])
        qr.make(fit=True)
        
        # Create image
        img = qr.make_image(fill_color="black", back_color="white")
        
        # Save QR code
        qr_path = qr_dir / info["filename"]
        img.save(qr_path)
        
        print(f"✅ {info['description']}: {qr_path}")
        print(f"   📱 URL: {info['url']}")
    
    print("\n" + "=" * 50)
    print("🎯 LOCAL TESTING READY!")
    print("=" * 50)
    print("📱 Download APK QR: maya_chatbot_LOCAL_download_qr.png")
    print("📄 Download Page QR: maya_chatbot_LOCAL_page_qr.png")
    print(f"🌐 Server running at: {base_url}")
    print("\n📋 How to test:")
    print("1. Make sure server is running: python start_distribution_server.py")
    print("2. Scan QR codes with your phone")
    print("3. Download and install APK")
    print("4. Test Maya Chatbot!")
    
    return True

if __name__ == "__main__":
    create_local_qr_codes() 