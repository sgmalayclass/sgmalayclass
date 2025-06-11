# 🌺 Oral Malay Chatbot / Chatbot Bahasa Melayu Lisan

A friendly AI chatbot designed to help you practice conversational Malay language with English translations and pronunciation guides.

**Chatbot AI yang mesra untuk membantu anda berlatih perbualan bahasa Melayu dengan terjemahan Inggeris dan panduan sebutan.**

## ✨ Features / Ciri-ciri

### Basic Version (`oral_malay_chatbot.py`)
- ✅ **Text-based conversations** - Perbualan berdasarkan teks
- ✅ **Malay responses with English translations** - Jawapan Melayu dengan terjemahan Inggeris  
- ✅ **Context-aware responses** - Jawapan mengikut konteks
- ✅ **Encouragement system** - Sistem galakan
- ✅ **Multiple conversation topics** - Pelbagai topik perbualan

### Enhanced Version (`oral_malay_chatbot_with_speech.py`)
- 🔊 **Text-to-speech (TTS)** - Teks kepada suara
- 🎤 **Speech recognition** - Pengecaman suara
- 🗣️ **Pronunciation guides** - Panduan sebutan
- 🎵 **Voice commands** - Arahan suara
- 🔄 **Bilingual support** - Sokongan dwibahasa

## 🚀 Quick Start / Mula Pantas

### 1. Basic Setup
```bash
# Navigate to project directory
cd "Python project"

# Run basic chatbot (no additional dependencies needed)
python oral_malay_chatbot.py
```

### 2. Enhanced Setup (with speech features)
```bash
# Install speech dependencies
pip install pyttsx3 SpeechRecognition

# For microphone input (may need additional setup on Windows)
pip install pyaudio

# Run enhanced chatbot
python oral_malay_chatbot_with_speech.py
```

## 💻 Installation / Pemasangan

### Option 1: Minimal Installation
No additional packages required! Just run the basic version.

### Option 2: Full Installation
```bash
# Install all dependencies
pip install -r requirements.txt

# Or install individually:
pip install pyttsx3
pip install SpeechRecognition
pip install pyaudio
```

### Windows PyAudio Issues?
If you get PyAudio installation errors on Windows:
```bash
# Try pre-compiled wheel
pip install pipwin
pipwin install pyaudio
```

## 🎯 How to Use / Cara Penggunaan

### Basic Commands / Arahan Asas
- **Start conversation**: Just type anything! / Taip apa sahaja!
- **Exit**: Type `quit`, `bye`, or `selamat tinggal`
- **Voice input** (enhanced): Type `speak`
- **Toggle voice**: Type `voice on` or `voice off`

### Sample Conversations / Contoh Perbualan

```
👤 You: Hello!
🤖 Maya: Apa khabar? Saya Maya!
     How are you? I'm Maya!
🗣️  Pronunciation: ah-pah kah-bar? sah-yah MY-ah

👤 You: I'm good
🤖 Maya: Bagus! Saya gembira mendengarnya.
     Good! I'm happy to hear that.

👤 You: What do you like to eat?
🤖 Maya: Saya suka makan nasi lemak! Anda suka apa?
     I like eating nasi lemak! What do you like?
```

## 📚 Topics Covered / Topik yang Diliputi

- **Greetings** - Salam dan ucapan
- **Daily conversation** - Perbualan harian  
- **Food and meals** - Makanan dan hidangan
- **Family** - Keluarga
- **Weather** - Cuaca
- **Feelings and emotions** - Perasaan dan emosi
- **Learning and study** - Pembelajaran dan kajian

## 🛠️ Customization / Penyesuaian

### Adding New Responses / Menambah Jawapan Baru
Edit the `responses` dictionary in the chatbot file:

```python
'new_topic': [
    ("Malay phrase", "English translation", "pronunciation guide"),
    # Add more responses...
]
```

### Adding New Keywords / Menambah Kata Kunci Baru
Edit the `keywords` dictionary:

```python
'new_topic': ['keyword1', 'keyword2', 'kata kunci']
```

## 🌐 Sharing with Classmates / Berkongsi dengan Rakan Sekelas

### Method 1: Share Files
1. Zip the Python files and `requirements.txt`
2. Share via email or cloud storage
3. Classmates run: `python oral_malay_chatbot.py`

### Method 2: GitHub (Recommended)
1. Create a repository
2. Upload the chatbot files
3. Share the GitHub link
4. Classmates can clone and run

### Method 3: Web Interface (Advanced)
Create a simple web interface using Streamlit:
```bash
pip install streamlit
# Then create a web version for easy sharing
```

## 🎓 Educational Benefits / Manfaat Pendidikan

- **Vocabulary building** - Pembinaan kosa kata
- **Pronunciation practice** - Latihan sebutan
- **Conversational confidence** - Keyakinan berperbualan
- **Cultural context** - Konteks budaya
- **Interactive learning** - Pembelajaran interaktif

## 🔧 Troubleshooting / Penyelesaian Masalah

### Common Issues / Isu Biasa

**Speech not working?**
- Check microphone permissions
- Try: `pip install --upgrade SpeechRecognition`
- Ensure internet connection (for Google Speech API)

**TTS not working?**
- Try: `pip install --upgrade pyttsx3`
- Check system audio settings
- Try different voice settings

**Import errors?**
- Run: `pip install -r requirements.txt`
- Check Python version (3.7+ recommended)

## 📖 Learning Tips / Tips Pembelajaran

1. **Start simple** - Use basic greetings first
2. **Practice daily** - 10-15 minutes per day
3. **Listen and repeat** - Use the pronunciation guides
4. **Don't be shy** - Make mistakes and learn!
5. **Use voice features** - Practice speaking out loud

## 🤝 Contributing / Menyumbang

Want to improve the chatbot? You can:
- Add more Malay phrases and responses
- Improve pronunciation guides
- Add new conversation topics
- Create a web interface
- Add gamification features

## 📞 Support / Sokongan

If you need help:
1. Check this README first
2. Try the troubleshooting section
3. Ask classmates who have it working
4. Search online for specific error messages

## 🌟 Future Features / Ciri Masa Hadapan

Ideas for enhancement:
- [ ] Grammar correction
- [ ] Lesson plans integration
- [ ] Progress tracking
- [ ] Multiplayer conversations
- [ ] Mobile app version
- [ ] Integration with Anki flashcards

---

**Selamat belajar! Happy learning!** 🎉

Made with ❤️ for Malay language learners 