#!/usr/bin/env python3
"""
Local Distribution Server for Maya Chatbot
Starts a web server to test QR codes and distribution
"""

import http.server
import socketserver
import webbrowser
import os
from pathlib import Path
import threading
import time

def start_server():
    """Start local web server for distribution testing"""
    
    print("🌐 Starting Maya Chatbot Distribution Server...")
    print("=" * 50)
    
    # Change to qr_codes directory
    os.chdir("qr_codes")
    
    PORT = 8000
    
    class CustomHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
        def end_headers(self):
            self.send_header('Access-Control-Allow-Origin', '*')
            super().end_headers()
    
    try:
        with socketserver.TCPServer(("", PORT), CustomHTTPRequestHandler) as httpd:
            server_url = f"http://localhost:{PORT}"
            download_page = f"{server_url}/maya_chatbot_melayu_download.html"
            
            print(f"✅ Server started at: {server_url}")
            print(f"📱 Download page: {download_page}")
            print("\n📋 Available files:")
            for file in Path(".").glob("*"):
                if file.is_file():
                    print(f"  📄 {file.name}")
            
            print("\n🎯 Testing Instructions:")
            print("1. Open the download page in your browser")
            print("2. Test QR codes with your phone camera")
            print("3. Share the QR code images with others")
            print("4. Press Ctrl+C to stop server")
            
            # Auto-open browser
            def open_browser():
                time.sleep(1)
                try:
                    webbrowser.open(download_page)
                    print(f"\n🌐 Opened browser: {download_page}")
                except:
                    print(f"\n🌐 Please manually open: {download_page}")
            
            threading.Thread(target=open_browser, daemon=True).start()
            
            print(f"\n🚀 Server running on port {PORT}...")
            httpd.serve_forever()
            
    except KeyboardInterrupt:
        print("\n\n🛑 Server stopped by user")
    except Exception as e:
        print(f"\n❌ Server error: {e}")

if __name__ == "__main__":
    if not Path("qr_codes").exists():
        print("❌ QR codes directory not found. Run create_distribution.py first.")
    else:
        start_server() 