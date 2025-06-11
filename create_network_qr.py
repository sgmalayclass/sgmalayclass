#!/usr/bin/env python3
"""
Create Network QR Codes for Maya Chatbot
Generates QR codes using computer's IP address for phone access
"""

import qrcode
from pathlib import Path
import subprocess
import re

def get_computer_ip():
    """Get the computer's IP address"""
    try:
        result = subprocess.run(['ipconfig'], capture_output=True, text=True)
        ipv4_lines = [line for line in result.stdout.split('\n') if 'IPv4' in line]
        if ipv4_lines:
            ip_match = re.search(r'(\d+\.\d+\.\d+\.\d+)', ipv4_lines[0])
            if ip_match:
                return ip_match.group(1)
    except:
        pass
    return "192.168.1.170"  # Fallback to detected IP

def create_network_qr_codes():
    """Create QR codes pointing to network IP address"""
    print("📱 Creating Network QR Codes for Maya Chatbot...")
    print("=" * 50)
    
    # Get computer's IP address
    computer_ip = get_computer_ip()
    print(f"🌐 Computer IP: {computer_ip}")
    
    # Network server URLs
    base_url = f"http://{computer_ip}:8000"
    download_url = f"{base_url}/maya_chatbot_melayu_v1.0.0.apk"
    page_url = f"{base_url}/maya_chatbot_melayu_download.html"
    
    qr_codes = {
        "download": {
            "url": download_url,
            "filename": "maya_chatbot_NETWORK_download_qr.png",
            "description": "Direct APK Download (Network)"
        },
        "page": {
            "url": page_url, 
            "filename": "maya_chatbot_NETWORK_page_qr.png",
            "description": "Download Page (Network)"
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
    print("🎯 NETWORK QR CODES READY!")
    print("=" * 50)
    print("📱 Download APK QR: maya_chatbot_NETWORK_download_qr.png")
    print("📄 Download Page QR: maya_chatbot_NETWORK_page_qr.png")
    print(f"🌐 Server URL: {base_url}")
    print("\n📋 How to use:")
    print("1. Make sure your phone is on the same WiFi network")
    print("2. Keep the server running: python start_distribution_server.py")
    print("3. Scan QR codes with your phone camera")
    print("4. Download and install APK")
    print("5. Test Maya Chatbot!")
    
    print("\n🔧 Troubleshooting:")
    print(f"- Computer IP: {computer_ip}")
    print("- Phone must be on same WiFi as computer")
    print("- Windows Firewall may need to allow Python/port 8000")
    print("- Try turning off Windows Defender temporarily if needed")
    
    return base_url

if __name__ == "__main__":
    create_network_qr_codes() 