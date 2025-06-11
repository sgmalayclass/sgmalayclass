#!/usr/bin/env python3
"""
Deploy Maya Chatbot to GitHub Pages
Creates a public internet-accessible version
"""

import os
import shutil
import subprocess

def create_github_deployment():
    """Create GitHub Pages deployment"""
    print("🌐 Creating GitHub Pages Deployment...")
    print("=" * 50)
    
    # Create docs folder for GitHub Pages
    docs_dir = "docs"
    if os.path.exists(docs_dir):
        shutil.rmtree(docs_dir)
    os.makedirs(docs_dir)
    
    # Copy web app
    shutil.copy("maya_chatbot_webapp.html", f"{docs_dir}/index.html")
    print("✅ Copied web app as index.html")
    
    # Create a mobile-optimized version
    mobile_html = '''<!DOCTYPE html>
<html lang="ms">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="Maya Chatbot Melayu - Practice Bahasa Melayu conversations with Singapore context">
    <title>Maya Chatbot Melayu - Free Online</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: linear-gradient(135deg, #4CAF50, #2E7D32);
            min-height: 100vh;
            display: flex;
            flex-direction: column;
        }
        .header {
            background: rgba(255,255,255,0.95);
            padding: 15px;
            text-align: center;
            color: #2E7D32;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        .header h1 {
            font-size: 20px;
            margin-bottom: 5px;
        }
        .header p {
            font-size: 14px;
            opacity: 0.8;
        }
        .chat-container {
            flex: 1;
            padding: 20px;
            overflow-y: auto;
            display: flex;
            flex-direction: column;
            gap: 10px;
        }
        .message {
            max-width: 85%;
            padding: 12px 16px;
            border-radius: 18px;
            word-wrap: break-word;
            font-size: 16px;
            line-height: 1.4;
        }
        .user-message {
            background: #4CAF50;
            color: white;
            align-self: flex-end;
            margin-left: auto;
        }
        .bot-message {
            background: rgba(255,255,255,0.95);
            color: #2E7D32;
            align-self: flex-start;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        }
        .input-container {
            background: rgba(255,255,255,0.95);
            padding: 15px;
            display: flex;
            gap: 10px;
            box-shadow: 0 -2px 10px rgba(0,0,0,0.1);
        }
        #messageInput {
            flex: 1;
            padding: 12px;
            border: 2px solid #e0e0e0;
            border-radius: 25px;
            outline: none;
            font-size: 16px;
            transition: border-color 0.3s;
        }
        #messageInput:focus {
            border-color: #4CAF50;
        }
        #sendButton {
            padding: 12px 20px;
            background: #4CAF50;
            color: white;
            border: none;
            border-radius: 25px;
            cursor: pointer;
            font-weight: bold;
            font-size: 16px;
            transition: background 0.3s;
        }
        #sendButton:hover {
            background: #45a049;
        }
        .quick-replies {
            display: flex;
            flex-wrap: wrap;
            gap: 8px;
            margin: 10px 20px;
        }
        .quick-reply {
            background: rgba(255,255,255,0.9);
            color: #2E7D32;
            border: 2px solid rgba(255,255,255,0.5);
            padding: 8px 16px;
            border-radius: 20px;
            cursor: pointer;
            font-size: 14px;
            transition: all 0.3s;
        }
        .quick-reply:hover {
            background: white;
            transform: translateY(-1px);
        }
        .typing-indicator {
            display: none;
            align-self: flex-start;
            background: rgba(255,255,255,0.9);
            padding: 12px 16px;
            border-radius: 18px;
            color: #666;
            font-style: italic;
        }
        @media (max-width: 480px) {
            .message {
                max-width: 90%;
                font-size: 15px;
            }
            #messageInput, #sendButton {
                font-size: 16px; /* Prevents zoom on iOS */
            }
        }
    </style>
</head>
<body>
    <div class="header">
        <h1>🇸🇬 Maya Chatbot Melayu</h1>
        <p>Practice Bahasa Melayu with Singapore context • Free & Online</p>
    </div>
    
    <div class="chat-container" id="chatContainer">
        <div class="message bot-message">
            Selamat datang! Saya Maya. Mari bercakap dalam Bahasa Melayu! 😊<br>
            <small>Saya boleh membantu dengan sapaan, makanan, keluarga, dan topik Singapore!</small>
        </div>
        
        <div class="typing-indicator" id="typingIndicator">
            Maya sedang menaip...
        </div>
    </div>
    
    <div class="quick-replies">
        <button class="quick-reply" onclick="sendQuickReply('Selamat pagi!')">Selamat pagi!</button>
        <button class="quick-reply" onclick="sendQuickReply('Apa khabar?')">Apa khabar?</button>
        <button class="quick-reply" onclick="sendQuickReply('Nak makan apa?')">Nak makan apa?</button>
        <button class="quick-reply" onclick="sendQuickReply('Berapa harga?')">Berapa harga?</button>
    </div>
    
    <div class="input-container">
        <input type="text" id="messageInput" placeholder="Taip mesej anda dalam Bahasa Melayu..." 
               onkeypress="if(event.key==='Enter') sendMessage()">
        <button id="sendButton" onclick="sendMessage()">Hantar</button>
    </div>

    <script>
        const responses = [
            // Greetings
            "Selamat pagi! Apa khabar hari ni?",
            "Baik, terima kasih! Semoga hari yang baik untuk awak!",
            "Wah, best! Hari ni cuaca panas betul!",
            
            // Food
            "Saya suka nasi lemak! Sedap sangat tau!",
            "Kat mana nak beli chicken rice yang sedap?",
            "Alamak, saya pun lapar dah! Jom makan!",
            "Wah, laksa Singapore memang best!",
            "Berapa harga teh tarik satu?",
            
            // Family & Daily
            "Keluarga awak sihat semua?",
            "Anak-anak dah balik sekolah ke?",
            "Weekend nak pergi mana?",
            "Kerja hari ni macam mana?",
            
            // Singapore context
            "MRT hari ni ramai sangat!",
            "HDB flat awak kat mana?",
            "Void deck ada program tak?",
            "Hawker center mana yang best?",
            
            // Responses
            "Betul tu! Saya setuju!",
            "Okay, jumpa nanti ye!",
            "Salam! Selamat tinggal!",
            "Terima kasih banyak-banyak!",
            "Sama-sama! Jaga diri ye!",
            "Insya'Allah, moga dipermudahkan!"
        ];

        function showTyping() {
            const typing = document.getElementById('typingIndicator');
            typing.style.display = 'block';
            setTimeout(() => {
                typing.style.display = 'none';
            }, 1500);
        }

        function addMessage(text, isUser) {
            const chatContainer = document.getElementById('chatContainer');
            const messageDiv = document.createElement('div');
            messageDiv.className = `message ${isUser ? 'user-message' : 'bot-message'}`;
            messageDiv.innerHTML = text;
            
            chatContainer.insertBefore(messageDiv, document.getElementById('typingIndicator'));
            chatContainer.scrollTop = chatContainer.scrollHeight;
        }

        function sendMessage() {
            const input = document.getElementById('messageInput');
            const message = input.value.trim();
            if (message) {
                addMessage(message, true);
                input.value = '';
                
                showTyping();
                setTimeout(() => {
                    const response = responses[Math.floor(Math.random() * responses.length)];
                    addMessage(response, false);
                }, 1000 + Math.random() * 1000);
            }
        }

        function sendQuickReply(message) {
            addMessage(message, true);
            showTyping();
            setTimeout(() => {
                const response = responses[Math.floor(Math.random() * responses.length)];
                addMessage(response, false);
            }, 800 + Math.random() * 800);
        }

        // Auto-focus on mobile
        window.addEventListener('load', () => {
            if (window.innerWidth > 768) {
                document.getElementById('messageInput').focus();
            }
        });
    </script>
</body>
</html>'''
    
    with open(f"{docs_dir}/index.html", "w", encoding="utf-8") as f:
        f.write(mobile_html)
    
    # Create README for GitHub
    readme_content = '''# Maya Chatbot Melayu 🇸🇬

A free online Malay chatbot for practicing Bahasa Melayu with Singapore context.

## 🌐 Live Demo
**Access anywhere:** https://[YOUR-USERNAME].github.io/[REPO-NAME]/

## ✨ Features
- Practice conversational Bahasa Melayu
- Singapore cultural context (HDB, MRT, hawker centers)
- Topics: Greetings, food, family, daily life
- Mobile-friendly responsive design
- Works on all devices with internet

## 🚀 Setup Instructions
1. Fork this repository
2. Go to Settings → Pages
3. Set source to "Deploy from branch: main /docs"
4. Your app will be live at: `https://[username].github.io/[repo-name]/`

## 📱 Usage
- Works over cellular data & WiFi
- No installation needed
- Add to home screen for app-like experience

## 🛠️ Built With
- Pure HTML5, CSS3, JavaScript
- No dependencies or frameworks
- Responsive design for all screen sizes

---
Made with ❤️ for the Singapore Malay community
'''
    
    with open(f"{docs_dir}/README.md", "w") as f:
        f.write(readme_content)
    
    print("✅ Created GitHub Pages structure in /docs")
    print("✅ Created mobile-optimized version")
    print("✅ Created README with instructions")
    
    return docs_dir

def create_instructions():
    """Create deployment instructions"""
    instructions = '''
# 🌐 INTERNET DEPLOYMENT OPTIONS

## Option 1: GitHub Pages (FREE & PERMANENT)
1. Create GitHub account: https://github.com
2. Create new repository: "maya-chatbot"
3. Upload /docs folder contents
4. Go to Settings → Pages
5. Set source: "Deploy from branch: main /docs"
6. Get URL: https://[username].github.io/maya-chatbot/

## Option 2: ngrok (TEMPORARY TUNNEL)
1. Download: https://ngrok.com/download
2. Run: `python -m http.server 8000`
3. Run: `ngrok http 8000`
4. Get public URL: https://abc123.ngrok.io

## Option 3: Netlify (FREE HOSTING)
1. Go to: https://netlify.com
2. Drag /docs folder to deploy
3. Get instant URL: https://random-name.netlify.app

## Option 4: Cloud Storage Sharing
1. Upload maya_chatbot_webapp.html to Google Drive
2. Set sharing to "Anyone with link"
3. Share link - works on any phone!

## ✅ RECOMMENDED: GitHub Pages
- Free forever
- Custom domain support
- Automatic HTTPS
- Works worldwide over cellular data
'''
    
    with open("INTERNET_DEPLOYMENT.md", "w") as f:
        f.write(instructions)
    
    print("✅ Created: INTERNET_DEPLOYMENT.md")

def main():
    """Main function"""
    print("🌐 Creating Internet-Accessible Maya Chatbot...")
    print("=" * 50)
    
    docs_dir = create_github_deployment()
    create_instructions()
    
    print("\n🎉 INTERNET SOLUTIONS READY!")
    print("=" * 50)
    print("📁 GitHub Pages files: /docs folder")
    print("📄 Instructions: INTERNET_DEPLOYMENT.md")
    print("🌐 Web app: /docs/index.html")
    
    print("\n🚀 NEXT STEPS:")
    print("1. Create GitHub repository")
    print("2. Upload /docs folder")
    print("3. Enable GitHub Pages")
    print("4. Get public URL that works over cellular!")
    
    print("\n💡 QUICK TEST:")
    print("Open maya_chatbot_webapp.html locally first to test!")

if __name__ == "__main__":
    main() 