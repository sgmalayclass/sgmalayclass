#!/usr/bin/env python3
"""
Malay Chatbot Mobile App - Kivy Version
Converts the existing Malay chatbot to a mobile-friendly APK
"""

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.popup import Popup
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.metrics import dp
from kivy.core.text import LabelBase

import json
import random
import re
from datetime import datetime
from typing import Dict, List, Tuple

# Security imports
from security_utils import sanitize_user_input, validate_json_data
from secure_storage import SecureStorage

# Register Malay-friendly fonts
try:
    LabelBase.register(name='MalayFont', 
                      fn_regular='fonts/NotoSans-Regular.ttf')
except:
    pass

class MalayChatbotApp(App):
    def build(self):
        # Set window properties for mobile
        Window.size = (350, 600)
        Window.clearcolor = (0.95, 0.95, 0.95, 1)
        
        # Load training data
        self.load_training_data()
        self.conversation_history = []
        self.context_stack = []
        
        # Main layout
        main_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # Header
        header = BoxLayout(orientation='horizontal', size_hint_y=None, height=dp(60))
        title = Label(text='🇸🇬 Maya - Chatbot Melayu Singapore!\n\nApa khabar hari ini? Jom kita berbual!', 
                     font_size='18sp', 
                     color=(0.2, 0.4, 0.8, 1),
                     bold=True)
        
        # Settings button
        settings_btn = Button(text='⚙️', 
                            size_hint=(None, None), 
                            size=(dp(50), dp(50)))
        settings_btn.bind(on_press=self.show_settings)
        
        header.add_widget(title)
        header.add_widget(settings_btn)
        
        # Chat area
        self.chat_scroll = ScrollView()
        self.chat_layout = GridLayout(cols=1, spacing=10, size_hint_y=None)
        self.chat_layout.bind(minimum_height=self.chat_layout.setter('height'))
        self.chat_scroll.add_widget(self.chat_layout)
        
        # Initial welcome message
        self.add_message("Maya", "🇸🇬 Selamat datang! Saya Maya, chatbot Bahasa Melayu Singapore!\n\nApa khabar hari ini? Jom kita berbual!", is_bot=True)
        
        # Input area
        input_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=dp(60))
        
        # Text input
        self.text_input = TextInput(
            hint_text='Taip mesej anda...',
            multiline=False,
            font_size='16sp',
            background_color=(1, 1, 1, 1)
        )
        self.text_input.bind(on_text_validate=self.send_message)
        
        # Send button
        send_btn = Button(
            text='📤',
            size_hint=(None, None),
            size=(dp(60), dp(60)),
            background_color=(0.2, 0.7, 0.3, 1)
        )
        send_btn.bind(on_press=self.send_message)
        
        # Quick reply buttons
        quick_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=dp(40), spacing=5)
        
        quick_buttons = [
            ("Apa khabar?", "greeting"),
            ("Makan apa?", "food"),
            ("Ajar saya", "learning"),
            ("Bye!", "goodbye")
        ]
        
        for text, category in quick_buttons:
            btn = Button(text=text, font_size='12sp', background_color=(0.8, 0.9, 1, 1))
            btn.bind(on_press=lambda x, txt=text: self.quick_reply(txt))
            quick_layout.add_widget(btn)
        
        input_layout.add_widget(self.text_input)
        input_layout.add_widget(send_btn)
        
        # Add all components
        main_layout.add_widget(header)
        main_layout.add_widget(self.chat_scroll)
        main_layout.add_widget(quick_layout)
        main_layout.add_widget(input_layout)
        
        return main_layout
    
    def load_training_data(self):
        """Load training data with security validation"""
        try:
            with open('malay_training_data.json', 'r', encoding='utf-8') as f:
                raw_data = f.read()
                if validate_json_data(raw_data):
                    self.training_data = json.loads(raw_data)
                else:
                    self._load_fallback_data()
        except:
            self._load_fallback_data()
    
    def _load_fallback_data(self):
        """Load fallback training data"""
        self.training_data = {
            "greetings": [
                {"user": "Apa khabar?", "bot": "Khabar baik! Awak macam mana hari ini?"},
                {"user": "Hello", "bot": "Hi! Selamat datang! Mari kita berbual dalam Bahasa Melayu!"}
            ],
            "food_ordering": [
                {"user": "Saya lapar", "bot": "Nak makan apa? Ada nasi lemak, mee goreng, roti prata!"},
                {"user": "Berapa harga roti prata?", "bot": "Roti prata kosong $1.20, roti telur $1.80. Nak order berapa keping?"}
            ],
            "goodbye": [
                {"user": "Bye", "bot": "Selamat tinggal! Jumpa lagi nanti! 👋"},
                {"user": "Sampai jumpa", "bot": "Sampai jumpa! Jaga diri baik-baik! 🇸🇬"}
            ]
        }
    
    def add_message(self, sender, message, is_bot=False):
        """Add message to chat area"""
        message_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=dp(80))
        
        if is_bot:
            # Bot message (left aligned)
            avatar = Label(text='🤖', size_hint=(None, None), size=(dp(40), dp(40)))
            message_bg = (0.9, 0.95, 1, 1)
            text_color = (0.1, 0.1, 0.1, 1)
        else:
            # User message (right aligned)
            avatar = Label(text='👤', size_hint=(None, None), size=(dp(40), dp(40)))
            message_bg = (0.2, 0.7, 0.3, 1)
            text_color = (1, 1, 1, 1)
        
        message_label = Label(
            text=f"[b]{sender}[/b]\n{message}",
            markup=True,
            text_size=(dp(250), None),
            halign='left',
            valign='top',
            color=text_color,
            font_size='14sp'
        )
        message_label.bind(texture_size=message_label.setter('size'))
        
        if is_bot:
            message_layout.add_widget(avatar)
            message_layout.add_widget(message_label)
            message_layout.add_widget(Label())  # Spacer
        else:
            message_layout.add_widget(Label())  # Spacer
            message_layout.add_widget(message_label)
            message_layout.add_widget(avatar)
        
        self.chat_layout.add_widget(message_layout)
        
        # Auto-scroll to bottom
        Clock.schedule_once(lambda dt: setattr(self.chat_scroll, 'scroll_y', 0), 0.1)
    
    def quick_reply(self, text):
        """Handle quick reply buttons"""
        self.text_input.text = text
        self.send_message(None)
    
    def send_message(self, instance):
        """Send user message and get bot response"""
        user_message = sanitize_user_input(self.text_input.text.strip())
        
        # Validate input length and content
        if not user_message or len(user_message) > 500:
            return
        
        # Add user message to chat
        self.add_message("You", user_message)
        
        # Get bot response
        bot_response = self.get_bot_response(user_message)
        
        # Add bot response to chat
        self.add_message("Maya", bot_response, is_bot=True)
        
        # Update conversation context
        self.update_context(user_message, bot_response)
        
        # Clear input
        self.text_input.text = ""
    
    def get_bot_response(self, user_input: str) -> str:
        """Generate bot response based on user input"""
        user_input_lower = user_input.lower()
        
        # Check each category in training data
        for category, items in self.training_data.items():
            for item in items:
                if isinstance(item, dict) and "user" in item and "bot" in item:
                    # Simple keyword matching
                    user_patterns = item["user"].lower()
                    if any(word in user_input_lower for word in user_patterns.split()):
                        return item["bot"]
        
        # Contextual responses based on keywords
        if any(word in user_input_lower for word in ["hello", "hai", "hi", "apa khabar"]):
            responses = [
                "Hai! Apa khabar? Saya Maya! 😊",
                "Selamat datang! Bagaimana hari anda?",
                "Hello! Senang berjumpa dengan anda! 🇸🇬"
            ]
            return random.choice(responses)
        
        elif any(word in user_input_lower for word in ["makan", "lapar", "food", "hungry"]):
            responses = [
                "Wah, lapar ya? Nak makan apa? Ada nasi lemak, laksa, roti prata! 🍜",
                "Jom pergi food court! Singapore ada banyak makanan sedap! 😋",
                "Saya suggest chicken rice atau bak chor mee - very Singaporean! 🇸🇬"
            ]
            return random.choice(responses)
        
        elif any(word in user_input_lower for word in ["bye", "goodbye", "sampai jumpa", "selamat tinggal"]):
            responses = [
                "Selamat tinggal! Jumpa lagi nanti! 👋",
                "Bye bye! Jaga diri baik-baik! 🇸🇬",
                "Sampai jumpa! Thanks for chatting with me! 😊"
            ]
            return random.choice(responses)
        
        elif any(word in user_input_lower for word in ["belajar", "ajar", "learn", "teach"]):
            responses = [
                "Bagus! Teruskan belajar Bahasa Melayu! Practice makes perfect! 📚",
                "Anda dah pandai! Jangan malu untuk cuba! Keep going! 💪",
                "Bahasa Melayu mudah sahaja. Saya boleh ajar anda! 🎓"
            ]
            return random.choice(responses)
        
        elif any(word in user_input_lower for word in ["singapore", "singapura", "hdb", "mrt"]):
            responses = [
                "Singapore memang best! Truly Asia in one island! 🇸🇬",
                "Majulah Singapura! Our little red dot is amazing! ❤️",
                "Singapore food, culture, people - semua best lah! 🏙️"
            ]
            return random.choice(responses)
        
        # Default responses
        default_responses = [
            "Menarik! Boleh cerita lebih detail? 🤔",
            "Oh begitu. Apa pendapat anda? 💭",
            "Saya faham. Apa lagi yang anda nak kongsi? 😊",
            "Betul ke? Cerita lagi sikit! 👂",
            "Wah, interesting! Tell me more! 🗣️"
        ]
        return random.choice(default_responses)
    
    def update_context(self, user_input: str, bot_response: str):
        """Update conversation context"""
        context_entry = {
            'user': user_input,
            'bot': bot_response,
            'timestamp': datetime.now().isoformat()
        }
        self.context_stack.append(context_entry)
        
        # Keep only recent context (last 5 exchanges)
        if len(self.context_stack) > 5:
            self.context_stack.pop(0)
    
    def show_settings(self, instance):
        """Show settings popup"""
        content = BoxLayout(orientation='vertical', spacing=10)
        
        # About info
        about_text = """
🇸🇬 Maya - Chatbot Melayu Singapore

Version: 1.0.0
Developer: AI Assistant
Language: Bahasa Melayu (Singapore)

Features:
• Conversational Malay practice
• Singapore cultural context
• Offline functionality
• Quick reply buttons

Terima kasih for using Maya! 😊
        """
        
        about_label = Label(text=about_text, 
                           text_size=(dp(300), None),
                           halign='center')
        
        close_btn = Button(text='Tutup', size_hint_y=None, height=dp(50))
        
        content.add_widget(about_label)
        content.add_widget(close_btn)
        
        popup = Popup(title='Settings & About',
                     content=content,
                     size_hint=(0.9, 0.7))
        
        close_btn.bind(on_press=popup.dismiss)
        popup.open()

if __name__ == '__main__':
    MalayChatbotApp().run() 