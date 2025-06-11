#!/usr/bin/env python3
"""
APK Distribution System with QR Code Generator
Provides secure APK distribution with QR codes, download tracking, and version management
"""

import qrcode
import hashlib
import json
import os
from datetime import datetime
from pathlib import Path
from typing import Dict, List
import zipfile
import shutil

class APKDistributionSystem:
    def __init__(self, base_url: str = "https://your-domain.com"):
        self.base_url = base_url
        self.apk_directory = Path("./apk_releases")
        self.distribution_data = Path("./distribution_data.json")
        self.qr_codes_dir = Path("./qr_codes")
        
        # Create directories
        self.apk_directory.mkdir(exist_ok=True)
        self.qr_codes_dir.mkdir(exist_ok=True)
        
        # Load existing distribution data
        self.load_distribution_data()
    
    def load_distribution_data(self):
        """Load existing distribution data or create new"""
        if self.distribution_data.exists():
            with open(self.distribution_data, 'r') as f:
                self.data = json.load(f)
        else:
            self.data = {
                "apps": {},
                "downloads": [],
                "analytics": {
                    "total_downloads": 0,
                    "downloads_by_version": {},
                    "downloads_by_date": {}
                }
            }
            self.save_distribution_data()
    
    def save_distribution_data(self):
        """Save distribution data to file"""
        with open(self.distribution_data, 'w') as f:
            json.dump(self.data, f, indent=2, default=str)
    
    def calculate_file_hash(self, file_path: Path) -> str:
        """Calculate SHA256 hash of APK file"""
        sha256_hash = hashlib.sha256()
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                sha256_hash.update(chunk)
        return sha256_hash.hexdigest()
    
    def add_apk(self, apk_path: str, app_name: str, version: str, description: str = "") -> Dict:
        """Add new APK to distribution system"""
        apk_file = Path(apk_path)
        if not apk_file.exists():
            raise FileNotFoundError(f"APK file not found: {apk_path}")
        
        # Calculate file hash and size
        file_hash = self.calculate_file_hash(apk_file)
        file_size = apk_file.stat().st_size
        
        # Create versioned filename
        safe_name = app_name.replace(" ", "_").lower()
        versioned_filename = f"{safe_name}_v{version}.apk"
        destination = self.apk_directory / versioned_filename
        
        # Copy APK to distribution directory
        shutil.copy2(apk_file, destination)
        
        # Create app entry if doesn't exist
        if app_name not in self.data["apps"]:
            self.data["apps"][app_name] = {
                "versions": {},
                "latest_version": version,
                "total_downloads": 0,
                "created_date": datetime.now().isoformat()
            }
        
        # Add version info
        version_info = {
            "version": version,
            "filename": versioned_filename,
            "file_path": str(destination),
            "file_hash": file_hash,
            "file_size": file_size,
            "description": description,
            "upload_date": datetime.now().isoformat(),
            "download_count": 0,
            "download_url": f"{self.base_url}/download/{versioned_filename}",
            "install_url": f"intent://download/{versioned_filename}#Intent;scheme=https;package=com.android.chrome;end"
        }
        
        self.data["apps"][app_name]["versions"][version] = version_info
        self.data["apps"][app_name]["latest_version"] = version
        
        self.save_distribution_data()
        return version_info
    
    def generate_qr_code(self, app_name: str, version: str = None, qr_type: str = "download") -> str:
        """Generate QR code for app download or install"""
        if app_name not in self.data["apps"]:
            raise ValueError(f"App '{app_name}' not found")
        
        if version is None:
            version = self.data["apps"][app_name]["latest_version"]
        
        if version not in self.data["apps"][app_name]["versions"]:
            raise ValueError(f"Version '{version}' not found for app '{app_name}'")
        
        version_info = self.data["apps"][app_name]["versions"][version]
        
        # Create QR code content based on type
        if qr_type == "download":
            qr_content = version_info["download_url"]
        elif qr_type == "install":
            qr_content = version_info["install_url"]
        elif qr_type == "info":
            qr_content = f"{self.base_url}/app/{app_name.replace(' ', '_').lower()}/v{version}"
        else:
            raise ValueError("QR type must be 'download', 'install', or 'info'")
        
        # Generate QR code
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(qr_content)
        qr.make(fit=True)
        
        # Create QR code image
        img = qr.make_image(fill_color="black", back_color="white")
        
        # Save QR code
        safe_name = app_name.replace(" ", "_").lower()
        qr_filename = f"{safe_name}_v{version}_{qr_type}_qr.png"
        qr_path = self.qr_codes_dir / qr_filename
        img.save(qr_path)
        
        return str(qr_path)
    
    def generate_distribution_page(self, app_name: str) -> str:
        """Generate HTML distribution page for an app"""
        if app_name not in self.data["apps"]:
            raise ValueError(f"App '{app_name}' not found")
        
        app_data = self.data["apps"][app_name]
        latest_version = app_data["versions"][app_data["latest_version"]]
        
        html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{app_name} - Download</title>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            max-width: 600px;
            margin: 0 auto;
            padding: 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            color: white;
        }}
        .container {{
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(10px);
            border-radius: 20px;
            padding: 30px;
            box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
            border: 1px solid rgba(255, 255, 255, 0.18);
        }}
        .app-icon {{
            width: 80px;
            height: 80px;
            background: #4CAF50;
            border-radius: 16px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 36px;
            margin: 0 auto 20px;
        }}
        .app-title {{
            font-size: 28px;
            font-weight: bold;
            text-align: center;
            margin-bottom: 10px;
        }}
        .app-version {{
            text-align: center;
            opacity: 0.8;
            margin-bottom: 30px;
        }}
        .download-section {{
            background: rgba(255, 255, 255, 0.1);
            border-radius: 15px;
            padding: 20px;
            margin: 20px 0;
            text-align: center;
        }}
        .download-btn {{
            background: #4CAF50;
            color: white;
            padding: 15px 30px;
            border: none;
            border-radius: 25px;
            font-size: 18px;
            font-weight: bold;
            text-decoration: none;
            display: inline-block;
            margin: 10px;
            box-shadow: 0 4px 15px 0 rgba(76, 175, 80, 0.3);
            transition: all 0.3s ease;
        }}
        .download-btn:hover {{
            transform: translateY(-2px);
            box-shadow: 0 6px 20px 0 rgba(76, 175, 80, 0.4);
        }}
        .qr-code {{
            background: white;
            padding: 20px;
            border-radius: 15px;
            margin: 20px 0;
            text-align: center;
        }}
        .qr-code img {{
            max-width: 200px;
            height: auto;
        }}
        .info-section {{
            background: rgba(255, 255, 255, 0.1);
            border-radius: 15px;
            padding: 20px;
            margin: 20px 0;
        }}
        .info-item {{
            display: flex;
            justify-content: space-between;
            margin: 10px 0;
            padding: 10px 0;
            border-bottom: 1px solid rgba(255, 255, 255, 0.1);
        }}
        .warning {{
            background: rgba(255, 152, 0, 0.2);
            border: 1px solid rgba(255, 152, 0, 0.5);
            border-radius: 10px;
            padding: 15px;
            margin: 20px 0;
        }}
        .steps {{
            background: rgba(255, 255, 255, 0.1);
            border-radius: 15px;
            padding: 20px;
            margin: 20px 0;
        }}
        .step {{
            display: flex;
            align-items: center;
            margin: 15px 0;
        }}
        .step-number {{
            background: #4CAF50;
            color: white;
            width: 30px;
            height: 30px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: bold;
            margin-right: 15px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="app-icon">🇸🇬</div>
        <h1 class="app-title">{app_name}</h1>
        <p class="app-version">Version {latest_version['version']}</p>
        
        <div class="download-section">
            <h3>📱 Download APK</h3>
            <a href="{latest_version['download_url']}" class="download-btn">
                ⬇️ Download APK ({latest_version['file_size'] // 1024 // 1024} MB)
            </a>
        </div>
        
        <div class="qr-code">
            <h4 style="color: #333; margin-bottom: 15px;">📱 Scan QR Code to Download</h4>
            <div style="color: #666; font-size: 14px; margin-bottom: 15px;">
                Point your phone camera at this QR code
            </div>
            <!-- QR Code would be embedded here -->
        </div>
        
        <div class="warning">
            <h4>⚠️ Installation Requirements</h4>
            <p>This app requires installation from "Unknown Sources" to be enabled on your Android device.</p>
        </div>
        
        <div class="steps">
            <h3>📋 Installation Steps</h3>
            <div class="step">
                <div class="step-number">1</div>
                <div>Download the APK file to your Android device</div>
            </div>
            <div class="step">
                <div class="step-number">2</div>
                <div>Go to Settings > Security > Enable "Unknown Sources"</div>
            </div>
            <div class="step">
                <div class="step-number">3</div>
                <div>Open the downloaded APK file and tap "Install"</div>
            </div>
            <div class="step">
                <div class="step-number">4</div>
                <div>Launch {app_name} and start chatting in Malay!</div>
            </div>
        </div>
        
        <div class="info-section">
            <h3>ℹ️ App Information</h3>
            <div class="info-item">
                <span>Version:</span>
                <span>{latest_version['version']}</span>
            </div>
            <div class="info-item">
                <span>File Size:</span>
                <span>{latest_version['file_size'] // 1024 // 1024} MB</span>
            </div>
            <div class="info-item">
                <span>Last Updated:</span>
                <span>{latest_version['upload_date'][:10]}</span>
            </div>
            <div class="info-item">
                <span>Downloads:</span>
                <span>{latest_version['download_count']}</span>
            </div>
            <div class="info-item">
                <span>SHA256:</span>
                <span style="font-family: monospace; font-size: 12px; word-break: break-all;">
                    {latest_version['file_hash'][:16]}...
                </span>
            </div>
        </div>
        
        <div class="info-section">
            <h3>🇸🇬 About Maya Chatbot</h3>
            <p>{latest_version.get('description', 'Maya is a friendly Malay chatbot designed to help you practice conversational Bahasa Melayu with Singapore context. Learn greetings, food ordering, family conversations, and more!')}</p>
        </div>
    </div>
    
    <script>
        // Track download clicks
        document.querySelector('.download-btn').addEventListener('click', function() {{
            // Send analytics (implement according to your backend)
            console.log('Download started for {app_name} v{latest_version["version"]}');
        }});
    </script>
</body>
</html>
        """
        
        # Save HTML file
        safe_name = app_name.replace(" ", "_").lower()
        html_filename = f"{safe_name}_download.html"
        html_path = self.qr_codes_dir / html_filename
        
        with open(html_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        return str(html_path)
    
    def create_complete_distribution_package(self, app_name: str, apk_path: str, version: str, description: str = "") -> Dict:
        """Create complete distribution package with APK, QR codes, and HTML page"""
        
        # Add APK to system
        version_info = self.add_apk(apk_path, app_name, version, description)
        
        # Generate QR codes
        download_qr = self.generate_qr_code(app_name, version, "download")
        install_qr = self.generate_qr_code(app_name, version, "install")
        info_qr = self.generate_qr_code(app_name, version, "info")
        
        # Generate HTML page
        html_page = self.generate_distribution_page(app_name)
        
        # Create distribution package
        package_info = {
            "app_name": app_name,
            "version": version,
            "apk_info": version_info,
            "qr_codes": {
                "download": download_qr,
                "install": install_qr,
                "info": info_qr
            },
            "html_page": html_page,
            "distribution_url": f"{self.base_url}/app/{app_name.replace(' ', '_').lower()}"
        }
        
        return package_info
    
    def get_analytics(self) -> Dict:
        """Get download analytics"""
        return self.data["analytics"]
    
    def record_download(self, app_name: str, version: str, user_agent: str = "", ip_address: str = ""):
        """Record a download event"""
        download_event = {
            "app_name": app_name,
            "version": version,
            "timestamp": datetime.now().isoformat(),
            "user_agent": user_agent,
            "ip_address": ip_address
        }
        
        self.data["downloads"].append(download_event)
        self.data["analytics"]["total_downloads"] += 1
        
        # Update version-specific analytics
        if version not in self.data["analytics"]["downloads_by_version"]:
            self.data["analytics"]["downloads_by_version"][version] = 0
        self.data["analytics"]["downloads_by_version"][version] += 1
        
        # Update app-specific download count
        if app_name in self.data["apps"] and version in self.data["apps"][app_name]["versions"]:
            self.data["apps"][app_name]["versions"][version]["download_count"] += 1
            self.data["apps"][app_name]["total_downloads"] += 1
        
        # Update daily analytics
        today = datetime.now().date().isoformat()
        if today not in self.data["analytics"]["downloads_by_date"]:
            self.data["analytics"]["downloads_by_date"][today] = 0
        self.data["analytics"]["downloads_by_date"][today] += 1
        
        self.save_distribution_data()

def main():
    """Example usage of the APK Distribution System"""
    
    # Initialize distribution system
    distributor = APKDistributionSystem("https://maya-chatbot.com")
    
    # Example: Add Maya Chatbot APK
    try:
        # Create distribution package for Maya Chatbot
        package = distributor.create_complete_distribution_package(
            app_name="Maya Chatbot Melayu",
            apk_path="./bin/malaychatbot-1.0-debug.apk",  # Path to your built APK
            version="1.0.0",
            description="Maya is a friendly Malay chatbot designed to help you practice conversational Bahasa Melayu with Singapore context. Features include greetings, food ordering, family conversations, and cultural references specific to Singapore."
        )
        
        print("✅ Distribution package created successfully!")
        print(f"📱 APK: {package['apk_info']['filename']}")
        print(f"📋 HTML Page: {package['html_page']}")
        print(f"🔗 Distribution URL: {package['distribution_url']}")
        print("\n📱 QR Codes generated:")
        for qr_type, qr_path in package['qr_codes'].items():
            print(f"  {qr_type.title()}: {qr_path}")
        
        # Print sharing instructions
        print("\n" + "="*50)
        print("📤 SHARING INSTRUCTIONS")
        print("="*50)
        print("1. Upload APK file to your web server")
        print("2. Share QR codes via:")
        print("   - WhatsApp/Telegram")
        print("   - Print and display physically")
        print("   - Email/social media")
        print("3. Users scan QR code → Download APK → Install")
        print("4. No Play Store needed!")
        
    except FileNotFoundError:
        print("❌ APK file not found. Please build your APK first:")
        print("   For Kivy: buildozer android debug")
        print("   For React Native: expo build:android")

if __name__ == "__main__":
    main() 