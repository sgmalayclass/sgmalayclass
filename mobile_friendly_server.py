#!/usr/bin/env python3
"""
Maya Chatbot - Mobile-Friendly Distribution Server
Handles mobile connections properly with CORS and better error handling
"""

import http.server
import socketserver
import socket
import os
import sys
import threading
import time
import webbrowser

class MobileFriendlyHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        # Add CORS headers for mobile compatibility
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', '*')
        self.send_header('Cache-Control', 'no-cache, no-store, must-revalidate')
        self.send_header('Pragma', 'no-cache')
        self.send_header('Expires', '0')
        super().end_headers()

    def do_OPTIONS(self):
        self.send_response(200)
        self.end_headers()

    def log_message(self, format, *args):
        client_ip = self.client_address[0]
        timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
        print(f"📱 [{timestamp}] {client_ip} - {format % args}")

def get_local_ip():
    """Get the computer's local IP address"""
    try:
        # Connect to a remote server to get local IP
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
        s.close()
        return local_ip
    except:
        return "192.168.1.1"  # fallback

def check_firewall_status():
    """Check Windows Firewall and provide instructions"""
    print("\n🔥 FIREWALL CHECK:")
    print("=" * 50)
    try:
        import subprocess
        result = subprocess.run(['netsh', 'advfirewall', 'show', 'allprofiles', 'state'], 
                              capture_output=True, text=True)
        if "ON" in result.stdout.upper():
            print("⚠️  Windows Firewall is ON - this may block mobile connections!")
            print("\n🛡️  FIREWALL SOLUTIONS:")
            print("1. Temporarily disable Windows Firewall:")
            print("   • Open Windows Security → Firewall & network protection")
            print("   • Turn off all networks temporarily")
            print("\n2. Or allow Python through firewall:")
            print("   • Windows will likely prompt you when server starts")
            print("   • Click 'Allow access' when prompted")
            print("\n3. Or run this command as Administrator:")
            print('   netsh advfirewall firewall add rule name="Python Server" dir=in action=allow protocol=TCP localport=8000')
        else:
            print("✅ Windows Firewall appears to be OFF")
    except:
        print("⚠️  Could not check firewall status")
        print("🛡️  If mobile can't connect, try disabling Windows Firewall temporarily")

def main():
    PORT = 8000
    local_ip = get_local_ip()
    
    print("📱 Maya Chatbot - Mobile-Friendly Server")
    print("=" * 50)
    print(f"🌐 Computer IP: {local_ip}")
    print(f"🔗 Mobile URL: http://{local_ip}:{PORT}")
    print(f"💻 Local URL: http://localhost:{PORT}")
    
    # Check firewall
    check_firewall_status()
    
    # Change to project directory
    if os.path.exists("maya_chatbot_melayu_v1.0.0.apk"):
        print("✅ APK file found")
    else:
        print("❌ APK file not found - creating symlink...")
        if os.path.exists("bin/maya_chatbot_v1.0.0_real.apk"):
            import shutil
            shutil.copy("bin/maya_chatbot_v1.0.0_real.apk", "maya_chatbot_melayu_v1.0.0.apk")
            print("✅ APK copied from bin folder")
    
    # Start server
    try:
        with socketserver.TCPServer(("", PORT), MobileFriendlyHandler) as httpd:
            print(f"\n🚀 Server starting on all interfaces (0.0.0.0:{PORT})")
            print("=" * 50)
            print("📱 MOBILE INSTRUCTIONS:")
            print(f"1. Scan QR code or type: http://{local_ip}:{PORT}")
            print("2. If 'site can't be reached', check firewall settings above")
            print("3. Make sure phone and computer are on same WiFi network")
            print("\n💻 COMPUTER ACCESS:")
            print(f"Open browser: http://localhost:{PORT}/maya_chatbot_melayu_download.html")
            print("\n🛑 Press Ctrl+C to stop server")
            print("=" * 50)
            
            # Auto-open browser after 2 seconds
            def open_browser():
                time.sleep(2)
                try:
                    webbrowser.open(f"http://localhost:{PORT}/maya_chatbot_melayu_download.html")
                    print("🌐 Opened browser automatically")
                except:
                    pass
            
            threading.Thread(target=open_browser, daemon=True).start()
            
            # Serve forever
            httpd.serve_forever()
            
    except KeyboardInterrupt:
        print("\n👋 Server stopped by user")
    except OSError as e:
        if "Address already in use" in str(e):
            print(f"❌ Port {PORT} is already in use!")
            print("Try running: taskkill /F /PID <process_id>")
        else:
            print(f"❌ Server error: {e}")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")

if __name__ == "__main__":
    main() 