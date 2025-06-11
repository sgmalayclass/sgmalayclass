# Maya Malay Chatbot - Mobile App Setup Guide

## 🚀 Overview
This guide will help you convert the Python-based Malay chatbot into mobile apps for Android and iPhone using the Kivy framework.

## 📱 Features in Mobile App
- ✅ **Chat Interface** - Clean, mobile-friendly chat UI
- ✅ **Vocabulary Quizzes** - Interactive multiple-choice quizzes
- ✅ **Role-play Scenarios** - Kopitiam and shopping scenarios
- ✅ **Context Memory** - Remembers conversation history
- ✅ **All Vocabulary** - Includes your 70+ daily conversation words
- ✅ **Touch-Friendly** - Optimized for mobile interaction

## 🛠️ Prerequisites

### For Development & Testing:
```bash
# Install Python 3.8+ 
# Install pip

# Install required packages
pip install -r requirements.txt
```

### For Android Build:
```bash
# Install buildozer
pip install buildozer

# Install Android SDK dependencies (Linux/Mac)
sudo apt-get install -y git zip unzip openjdk-8-jdk python3-pip autoconf libtool pkg-config zlib1g-dev libncurses5-dev libncursesw5-dev libtinfo5 cmake libffi-dev libssl-dev

# Install Android SDK & NDK (will be handled by buildozer)
```

### For iOS Build (Mac only):
```bash
# Install Xcode from App Store
# Install kivy-ios
pip install kivy-ios
```

## 🏃‍♂️ Quick Start

### 1. Test the App Locally
```bash
# Run the mobile app on desktop for testing
python main.py
```

### 2. Build for Android
```bash
# Initialize buildozer (first time only) 
buildozer init

# Build APK (debug version)
buildozer android debug

# The APK will be in: bin/malaychatbot-1.0-armeabi-v7a-debug.apk
```

### 3. Install on Android Device
```bash
# Enable Developer Options and USB Debugging on your phone
# Connect phone via USB

# Install directly to connected device
buildozer android debug deploy run

# Or manually install the APK file
adb install bin/malaychatbot-1.0-armeabi-v7a-debug.apk
```

### 4. Build for iOS (Mac only)
```bash
# Build iOS project
toolchain build python3 kivy

# Create Xcode project
kivy-ios create malaychatbot .

# Open in Xcode and build
open malaychatbot-ios/malaychatbot.xcodeproj
```

## 📁 Project Structure
```
malay-chatbot/
├── malay_chatbot_mobile_app.py    # Main mobile app code
├── main.py                        # Entry point for buildozer
├── buildozer.spec                 # Build configuration
├── requirements.txt               # Python dependencies
├── oral_malay_chatbot_with_speech.py  # Original desktop version
└── MOBILE_APP_SETUP.md           # This guide
```

## 🎯 Key Mobile App Features

### Chat Interface
- **Clean Design**: Mobile-optimized chat bubbles
- **Auto-scroll**: Automatically scrolls to latest messages
- **Touch Input**: Easy typing with mobile keyboard
- **Color Coding**: Blue for Maya, Green for user

### Interactive Menus
- **Quiz Menu**: Choose from categories (keluarga, makanan, percakapan_harian)
- **Role-play Menu**: Select scenarios (kopitiam, shopping)
- **Popup Dialogs**: Mobile-friendly selection interfaces

### Vocabulary System
- **70+ Daily Words**: All your conversation words included
- **Multiple Choice**: 4-option quizzes
- **Instant Feedback**: Immediate right/wrong indication
- **Category-based**: Organized learning topics

## 🔧 Customization Options

### Modify Colors
Edit `malay_chatbot_mobile_app.py`:
```python
# Change app colors
bot_color = get_color_from_hex('#2196F3')  # Bot messages
user_color = get_color_from_hex('#4CAF50')  # User messages
button_color = get_color_from_hex('#FF9800') # Buttons
```

### Add More Vocabulary
```python
# Add new categories in MalayChatbotCore.__init__()
self.word_categories['new_category'] = {
    'words': {
        'malay_word': 'english_translation',
        # ... more words
    }
}
```

### Add Role-play Scenarios
```python
# Add new scenarios
self.roleplay_scenarios['new_scenario'] = {
    'title': 'New Scenario Title',
    'starter': "Opening message in Malay"
}
```

## 📱 Platform-Specific Notes

### Android
- **Min SDK**: Android 5.0 (API 21)
- **Target SDK**: Android 13 (API 33)
- **Permissions**: Internet, Storage, Microphone
- **File Size**: ~20-30MB APK

### iOS
- **Min iOS**: iOS 10.0+
- **Languages**: Swift/Objective-C wrapper around Python
- **Signing**: Requires Apple Developer Account for distribution
- **File Size**: ~30-40MB IPA

## 🐛 Troubleshooting

### Common Issues:

1. **Build Fails - Missing Dependencies**
   ```bash
   # Install system dependencies
   sudo apt-get update
   sudo apt-get install build-essential
   ```

2. **Android SDK Not Found**
   ```bash
   # Let buildozer handle it automatically
   buildozer android debug
   ```

3. **App Crashes on Phone**
   ```bash
   # Check logs
   buildozer android debug deploy run logcat
   ```

4. **Speech Not Working**
   - TTS may not work on all devices
   - App will work without speech features

## 🚀 Release Process

### For Android Play Store:
```bash
# Build release APK
buildozer android release

# Sign the APK (requires keystore)
# Upload to Google Play Console
```

### For iOS App Store:
1. Build in Xcode
2. Archive and validate
3. Upload to App Store Connect
4. Submit for review

## 📊 Performance Tips

1. **Optimize Images**: Use PNG/JPG compression
2. **Reduce App Size**: Remove unused dependencies
3. **Memory Management**: Clear old chat messages periodically
4. **Battery Usage**: Minimize background processing

## 🔄 Updates & Maintenance

1. **Version Updates**: Modify `version = 1.1` in buildozer.spec
2. **Add Features**: Edit malay_chatbot_mobile_app.py
3. **Bug Fixes**: Test locally, then rebuild
4. **Store Updates**: Upload new APK/IPA to stores

## 💡 Advanced Features (Future Enhancements)

- **Offline Mode**: Cache vocabulary for offline use
- **Progress Tracking**: Save learning progress
- **Audio Recording**: Record and playback pronunciation
- **Notifications**: Daily vocabulary reminders
- **Social Features**: Share progress with friends

## 📞 Support

If you encounter issues:
1. Check the troubleshooting section
2. Review buildozer/kivy documentation
3. Test on multiple devices
4. Consider creating a Progressive Web App (PWA) as alternative

---

## ✅ Quick Checklist

- [ ] Install requirements: `pip install -r requirements.txt`
- [ ] Test locally: `python main.py`
- [ ] Build Android: `buildozer android debug`
- [ ] Test on device: Install APK
- [ ] (Optional) Build iOS: Use kivy-ios on Mac
- [ ] Customize colors/features as needed
- [ ] Prepare for app store release

**Your Maya Malay Chatbot mobile app is ready! 🎉** 