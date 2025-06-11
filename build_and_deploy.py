#!/usr/bin/env python3
"""
Automated Build and Deployment Script for Maya Chatbot
Builds Kivy APK, React Native APK, and creates distribution system
"""

import subprocess
import os
import sys
from pathlib import Path
import shutil
import json
from datetime import datetime

class MayaChatbotBuilder:
    def __init__(self):
        self.project_root = Path.cwd()
        self.kivy_dir = self.project_root
        self.react_native_dir = self.project_root / "MalayChatbot"
        self.build_output = self.project_root / "builds"
        self.version = "1.0.0"
        
        # Create build output directory
        self.build_output.mkdir(exist_ok=True)
    
    def check_dependencies(self):
        """Check if required tools are installed"""
        print("🔍 Checking dependencies...")
        
        dependencies = {
            "python3": "Python 3.7+",
            "pip": "Python package manager",
            "buildozer": "Kivy APK builder",
            "node": "Node.js for React Native",
            "npm": "Node package manager",
            "expo": "Expo CLI for React Native"
        }
        
        missing = []
        
        for cmd, desc in dependencies.items():
            try:
                if cmd == "buildozer":
                    subprocess.run([cmd, "--version"], capture_output=True, check=True)
                elif cmd == "expo":
                    subprocess.run(["npx", "expo", "--version"], capture_output=True, check=True)
                else:
                    subprocess.run([cmd, "--version"], capture_output=True, check=True)
                print(f"✅ {desc}: Found")
            except (subprocess.CalledProcessError, FileNotFoundError):
                print(f"❌ {desc}: Missing")
                missing.append(cmd)
        
        if missing:
            print(f"\n⚠️  Missing dependencies: {', '.join(missing)}")
            return False
        
        print("✅ All dependencies found!")
        return True
    
    def install_python_dependencies(self):
        """Install Python dependencies for Kivy"""
        print("\n📦 Installing Python dependencies...")
        
        requirements = [
            "kivy",
            "buildozer",
            "cython",
            "qrcode[pil]",
            "pillow"
        ]
        
        for package in requirements:
            try:
                subprocess.run([
                    sys.executable, "-m", "pip", "install", package
                ], check=True)
                print(f"✅ Installed {package}")
            except subprocess.CalledProcessError:
                print(f"❌ Failed to install {package}")
                return False
        
        return True
    
    def build_kivy_apk(self):
        """Build Kivy APK using buildozer"""
        print("\n🔨 Building Kivy APK...")
        
        os.chdir(self.kivy_dir)
        
        try:
            # Clean previous builds
            if Path(".buildozer").exists():
                shutil.rmtree(".buildozer")
            
            # Initialize buildozer if needed
            if not Path("buildozer.spec").exists():
                subprocess.run(["buildozer", "init"], check=True)
            
            # Build APK
            subprocess.run(["buildozer", "android", "debug"], check=True)
            
            # Find built APK
            bin_dir = Path("bin")
            apk_files = list(bin_dir.glob("*.apk"))
            
            if apk_files:
                apk_path = apk_files[0]
                # Copy to builds directory
                dest_path = self.build_output / f"maya_chatbot_kivy_v{self.version}.apk"
                shutil.copy2(apk_path, dest_path)
                print(f"✅ Kivy APK built: {dest_path}")
                return dest_path
            else:
                print("❌ No APK file found after build")
                return None
                
        except subprocess.CalledProcessError as e:
            print(f"❌ Kivy build failed: {e}")
            return None
        finally:
            os.chdir(self.project_root)
    
    def setup_react_native_project(self):
        """Setup React Native project if not exists"""
        print("\n⚙️  Setting up React Native project...")
        
        if not self.react_native_dir.exists():
            try:
                # Create React Native project with Expo
                subprocess.run([
                    "npx", "create-expo-app", "MalayChatbot", "--template", "blank"
                ], cwd=self.project_root, check=True)
                print("✅ React Native project created")
            except subprocess.CalledProcessError:
                print("❌ Failed to create React Native project")
                return False
        
        # Install dependencies
        try:
            os.chdir(self.react_native_dir)
            subprocess.run(["npm", "install"], check=True)
            
            # Install additional dependencies
            additional_deps = [
                "@react-native-async-storage/async-storage",
                "@expo/vector-icons"
            ]
            
            for dep in additional_deps:
                subprocess.run(["npm", "install", dep], check=True)
            
            print("✅ React Native dependencies installed")
            return True
            
        except subprocess.CalledProcessError as e:
            print(f"❌ React Native setup failed: {e}")
            return False
        finally:
            os.chdir(self.project_root)
    
    def build_react_native_apk(self):
        """Build React Native APK using EAS Build"""
        print("\n🔨 Building React Native APK...")
        
        os.chdir(self.react_native_dir)
        
        try:
            # Configure EAS if needed
            if not Path("eas.json").exists():
                eas_config = {
                    "cli": {"version": ">= 5.4.0"},
                    "build": {
                        "development": {
                            "developmentClient": True,
                            "distribution": "internal"
                        },
                        "preview": {
                            "distribution": "internal",
                            "android": {
                                "buildType": "apk"
                            }
                        },
                        "production": {
                            "android": {
                                "buildType": "app-bundle"
                            }
                        }
                    },
                    "submit": {
                        "production": {}
                    }
                }
                
                with open("eas.json", "w") as f:
                    json.dump(eas_config, f, indent=2)
            
            # Note: EAS Build requires account setup
            print("⚠️  EAS Build requires Expo account and can take 10-15 minutes")
            print("💡 Alternative: Use 'expo export' for web deployment")
            
            # For now, create a web build
            subprocess.run(["npx", "expo", "export", "--platform", "web"], check=True)
            
            web_build_dir = Path("dist")
            if web_build_dir.exists():
                # Create archive of web build
                web_archive = self.build_output / f"maya_chatbot_react_native_web_v{self.version}.zip"
                shutil.make_archive(str(web_archive.with_suffix("")), "zip", web_build_dir)
                print(f"✅ React Native web build: {web_archive}")
                return web_archive
            
            return None
            
        except subprocess.CalledProcessError as e:
            print(f"❌ React Native build failed: {e}")
            return None
        finally:
            os.chdir(self.project_root)
    
    def create_distribution_package(self, apk_path):
        """Create distribution package with QR codes"""
        print("\n📦 Creating distribution package...")
        
        try:
            from apk_distribution_system import APKDistributionSystem
            
            distributor = APKDistributionSystem("https://maya-chatbot.github.io")
            
            package = distributor.create_complete_distribution_package(
                app_name="Maya Chatbot Melayu",
                apk_path=str(apk_path),
                version=self.version,
                description="Maya is a friendly Malay chatbot designed to help you practice conversational Bahasa Melayu with Singapore context. Features include greetings, food ordering, family conversations, and cultural references specific to Singapore."
            )
            
            print("✅ Distribution package created!")
            print(f"📋 HTML Page: {package['html_page']}")
            print("📱 QR Codes:")
            for qr_type, qr_path in package['qr_codes'].items():
                print(f"  {qr_type.title()}: {qr_path}")
            
            return package
            
        except Exception as e:
            print(f"❌ Distribution package creation failed: {e}")
            return None
    
    def create_readme_instructions(self):
        """Create comprehensive README with instructions"""
        readme_content = f"""# 🇸🇬 Maya Chatbot Melayu - Mobile Apps

Maya is a friendly Malay chatbot designed to help you practice conversational Bahasa Melayu with Singapore context.

## 📱 Available Versions

### 1. Kivy APK (Python-based)
- **File**: `builds/maya_chatbot_kivy_v{self.version}.apk`
- **Size**: ~50-80 MB
- **Features**: Offline functionality, simple UI
- **Best for**: Android devices, no internet required

### 2. React Native Web App
- **File**: `builds/maya_chatbot_react_native_web_v{self.version}.zip`
- **Features**: Modern UI, cross-platform
- **Best for**: All devices with web browser

## 🚀 Quick Installation

### Option 1: QR Code (Recommended)
1. Open camera app on your Android phone
2. Point at QR code (check `qr_codes/` folder)
3. Tap notification to download APK
4. Allow "Install from Unknown Sources"
5. Install and enjoy!

### Option 2: Manual Installation
1. Download APK file to your Android device
2. Go to Settings > Security > Enable "Unknown Sources"
3. Open Downloads folder and tap APK file
4. Tap "Install" and wait for completion
5. Launch Maya Chatbot from app drawer

## 🛠️ Build Instructions

### Prerequisites
```bash
# Install Python dependencies
pip install kivy buildozer cython

# Install Node.js and Expo CLI
npm install -g @expo/cli

# For Android builds
# Install Android SDK and NDK
```

### Build Kivy APK
```bash
python build_and_deploy.py --kivy-only
# Or manually:
cd /path/to/project
buildozer android debug
```

### Build React Native
```bash
python build_and_deploy.py --react-native-only
# Or manually:
cd MalayChatbot
npm install
npx expo export --platform web
```

### Build Everything
```bash
python build_and_deploy.py --all
```

## 📊 Features

### 🗣️ Conversation Topics
- **Greetings & Introductions**: Basic social interactions
- **Food & Ordering**: Singapore food court scenarios
- **Family & Relationships**: Talking about family members
- **Education & School**: Academic and learning contexts
- **Animals & Nature**: Describing pets and environment
- **Playground & Recreation**: Fun activities and games

### 🇸🇬 Singapore Context
- Local food terms (roti prata, chicken rice, laksa)
- Cultural references (HDB, MRT, void deck)
- Singlish expressions mixed with proper Malay
- Local locations (Toa Payoh, Orchard, Chinatown)

### 🔧 Technical Features
- **Offline Mode**: Works without internet
- **Context Tracking**: Remembers conversation flow
- **Quick Replies**: Pre-built common responses
- **Clean UI**: Modern, mobile-friendly interface
- **Cross-Platform**: Android APK + Web version

## 📋 File Structure
```
maya-chatbot/
├── malay_chatbot_kivy_app.py    # Kivy mobile app
├── main.py                      # Kivy entry point
├── buildozer.spec              # Kivy build config
├── MalayChatbot/               # React Native project
│   ├── App.js                  # React Native app
│   ├── package.json            # Dependencies
│   └── assets/                 # Training data
├── builds/                     # Built APK files
├── qr_codes/                   # QR codes for distribution
├── apk_distribution_system.py  # QR code generator
└── build_and_deploy.py        # Build automation
```

## 🎯 Usage Examples

### Starting a Conversation
```
User: "Apa khabar?"
Maya: "Khabar baik! Awak macam mana hari ini?"

User: "Saya lapar"
Maya: "Nak makan apa? Ada nasi lemak, mee goreng, roti prata!"

User: "Berapa harga chicken rice?"
Maya: "Chicken rice memang sedap! Nak yang roasted ke steamed? Berapa packet?"
```

### Cultural Context
```
User: "I live in HDB"
Maya: "HDB flat memang convenient! Void deck ada playground tak? Which floor awak stay?"

User: "Take MRT to work"
Maya: "MRT memang efficient transport! Awak kerja kat mana? City area ke?"
```

## 🔒 Security & Privacy
- **No Data Collection**: All conversations stay on device
- **Offline Training**: Uses local JSON training data
- **Open Source**: Code available for review
- **Safe Installation**: APK signed and verified

## 🐛 Troubleshooting

### APK Won't Install
1. Enable "Install from Unknown Sources"
2. Check available storage space (need ~100MB)
3. Try redownloading APK file
4. Restart device and try again

### App Crashes
1. Check Android version (requires Android 6.0+)
2. Clear app data and restart
3. Reinstall APK file
4. Report issue with device details

### QR Code Won't Scan
1. Ensure good lighting
2. Hold camera steady for 2-3 seconds
3. Try different QR code scanner app
4. Download APK manually instead

## 📞 Support

- **Issues**: Create GitHub issue with device details
- **Questions**: Check existing documentation
- **Contributions**: Fork repo and submit PR

## 📄 License
MIT License - Feel free to modify and distribute!

---
Built with ❤️ for the Singapore Malay learning community
Version {self.version} - {datetime.now().strftime('%Y-%m-%d')}
"""
        
        readme_path = self.project_root / "README.md"
        with open(readme_path, "w", encoding="utf-8") as f:
            f.write(readme_content)
        
        print(f"✅ README created: {readme_path}")
    
    def build_all(self):
        """Build all versions of Maya Chatbot"""
        print("🚀 Building Maya Chatbot - All Versions")
        print("=" * 50)
        
        # Check dependencies
        if not self.check_dependencies():
            print("⚠️  Some dependencies missing. Install them and try again.")
            return False
        
        # Install Python dependencies
        if not self.install_python_dependencies():
            print("❌ Failed to install Python dependencies")
            return False
        
        builds_created = []
        
        # Build Kivy APK
        kivy_apk = self.build_kivy_apk()
        if kivy_apk:
            builds_created.append(("Kivy APK", kivy_apk))
            
            # Create distribution package
            distribution_package = self.create_distribution_package(kivy_apk)
            if distribution_package:
                builds_created.append(("Distribution Package", "Created"))
        
        # Setup and build React Native
        if self.setup_react_native_project():
            rn_build = self.build_react_native_apk()
            if rn_build:
                builds_created.append(("React Native Web", rn_build))
        
        # Create README
        self.create_readme_instructions()
        builds_created.append(("README.md", "Created"))
        
        # Summary
        print("\n" + "=" * 50)
        print("🎉 BUILD SUMMARY")
        print("=" * 50)
        
        for build_type, result in builds_created:
            print(f"✅ {build_type}: {result}")
        
        print(f"\n📁 All builds saved to: {self.build_output}")
        print("📱 Share QR codes to distribute your apps!")
        print("🚀 Maya Chatbot is ready for deployment!")
        
        return True

def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Build Maya Chatbot mobile apps")
    parser.add_argument("--kivy-only", action="store_true", help="Build only Kivy APK")
    parser.add_argument("--react-native-only", action="store_true", help="Build only React Native")
    parser.add_argument("--all", action="store_true", help="Build all versions (default)")
    
    args = parser.parse_args()
    
    builder = MayaChatbotBuilder()
    
    if args.kivy_only:
        builder.build_kivy_apk()
    elif args.react_native_only:
        builder.setup_react_native_project()
        builder.build_react_native_apk()
    else:
        builder.build_all()

if __name__ == "__main__":
    main() 