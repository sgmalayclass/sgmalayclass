#!/usr/bin/env python3
"""
Malay Learning Chatbot - Mobile App Version
A mobile-friendly chatbot for learning Singapore Malay with speech features.
Built with Kivy for Android and iOS deployment.
"""

import random
import json
import os
from datetime import datetime
from typing import Dict, List, Optional, Tuple
import threading

# Kivy imports
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.clock import Clock
from kivy.core.audio import SoundLoader
from kivy.utils import get_color_from_hex

# Import the unified core
from chatbot_core import MalayChatbotCore

# Try to import speech libraries
try:
    import pyttsx3
    SPEECH_AVAILABLE = True
except ImportError:
    SPEECH_AVAILABLE = False

try:
    from gtts import gTTS
    import tempfile
    GTTS_AVAILABLE = True
except ImportError:
    GTTS_AVAILABLE = False

class ChatScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Initialize the unified chatbot core
        self.chatbot = MalayChatbotCore()
        self.build_interface()
    
    def build_interface(self):
        """Build the chat interface"""
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # Header
        header = BoxLayout(orientation='horizontal', size_hint_y=None, height='60dp')
        title = Label(
            text='🇸🇬 Maya - Chatbot Bahasa Melayu Singapore',
            font_size='18sp',
            bold=True,
            color=(0.2, 0.4, 0.8, 1)
        )
        
        # Settings button
        settings_btn = Button(
            text='⚙️',
            size_hint=(None, None),
            size=('50dp', '50dp')
        )
        settings_btn.bind(on_press=self.show_settings_popup)
        
        header.add_widget(title)
        header.add_widget(settings_btn)
        
        # Chat area
        self.chat_scroll = ScrollView()
        self.chat_layout = GridLayout(
            cols=1,
            spacing=10,
            size_hint_y=None,
            padding=[10, 10]
        )
        self.chat_layout.bind(minimum_height=self.chat_layout.setter('height'))
        self.chat_scroll.add_widget(self.chat_layout)
        
        # Add welcome message
        self.add_chat_message("Maya", "Selamat datang! Apa khabar hari ini?", is_bot=True)
        
        # Control buttons
        control_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height='40dp')
        
        quiz_btn = Button(text='Quiz', background_color=(0.3, 0.7, 0.9, 1))
        quiz_btn.bind(on_press=self.start_quiz_mode)
        
        roleplay_btn = Button(text='Role Play', background_color=(0.9, 0.7, 0.3, 1))
        roleplay_btn.bind(on_press=self.show_roleplay_options)
        
        help_btn = Button(text='Help', background_color=(0.7, 0.9, 0.3, 1))
        help_btn.bind(on_press=self.show_help)
        
        control_layout.add_widget(quiz_btn)
        control_layout.add_widget(roleplay_btn)
        control_layout.add_widget(help_btn)
        
        # Input area
        input_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height='50dp')
        
        self.text_input = TextInput(
            hint_text='Taip mesej anda di sini...',
            multiline=False,
            font_size='16sp'
        )
        self.text_input.bind(on_text_validate=self.send_message)
        
        send_btn = Button(
            text='Send',
            size_hint=(None, None),
            size=('80dp', '50dp'),
            background_color=(0.2, 0.8, 0.2, 1)
        )
        send_btn.bind(on_press=self.send_message)
        
        input_layout.add_widget(self.text_input)
        input_layout.add_widget(send_btn)
        
        # Add all components
        layout.add_widget(header)
        layout.add_widget(self.chat_scroll)
        layout.add_widget(control_layout)
        layout.add_widget(input_layout)
        
        self.add_widget(layout)
    
    def add_chat_message(self, sender: str, message: str, is_bot: bool = False):
        """Add a message to the chat area"""
        message_layout = BoxLayout(
            orientation='horizontal',
            size_hint_y=None,
            height='80dp',
            padding=[5, 5]
        )
        
        # Create message label
        if is_bot:
            avatar = '🤖'
            bg_color = (0.9, 0.95, 1, 1)
            text_color = (0.1, 0.1, 0.1, 1)
        else:
            avatar = '👤'
            bg_color = (0.2, 0.7, 0.3, 1)
            text_color = (1, 1, 1, 1)
        
        avatar_label = Label(
            text=avatar,
            size_hint=(None, None),
            size=('40dp', '40dp'),
            font_size='20sp'
        )
        
        message_label = Label(
            text=f"[b]{sender}:[/b]\n{message}",
            markup=True,
            text_size=(None, None),
            halign='left',
            valign='middle',
            color=text_color,
            font_size='14sp'
        )
        
        if is_bot:
            message_layout.add_widget(avatar_label)
            message_layout.add_widget(message_label)
        else:
            message_layout.add_widget(message_label)
            message_layout.add_widget(avatar_label)
        
        self.chat_layout.add_widget(message_layout)
        
        # Auto scroll to bottom
        Clock.schedule_once(lambda dt: setattr(self.chat_scroll, 'scroll_y', 0), 0.1)
    
    def send_message(self, instance):
        """Send user message and get bot response"""
        user_message = self.text_input.text.strip()
        if not user_message:
            return
        
        # Add user message
        self.add_chat_message("You", user_message)
        
        # Get bot response using unified core
        malay_response, english_translation = self.chatbot.generate_response(user_message)
        
        # Format response with translation
        full_response = f"{malay_response}\n\n[i]({english_translation})[/i]"
        
        # Add bot response
        self.add_chat_message("Maya", full_response, is_bot=True)
        
        # Update context
        self.chatbot.update_context(user_message, malay_response)
        
        # Clear input
        self.text_input.text = ""
    
    def start_quiz_mode(self, instance):
        """Start quiz mode"""
        quiz = self.chatbot.generate_quiz()
        if quiz:
            self.chatbot.start_quiz_mode()
            quiz_text = f"Quiz: {quiz['question']}\n\n"
            for i, option in enumerate(quiz['options'], 1):
                quiz_text += f"{i}. {option}\n"
            
            self.add_chat_message("Maya", quiz_text, is_bot=True)
        else:
            self.add_chat_message("Maya", "Maaf, quiz tidak tersedia sekarang.", is_bot=True)
    
    def show_roleplay_options(self, instance):
        """Show role play options"""
        roleplay_message = """Mari berlakon! Pilih satu situasi:

1. Di kedai makan (At the restaurant)
2. Di pasar (At the market)
3. Tanya arah (Asking for directions)
4. Perkenalan diri (Self introduction)

Taip nombor yang anda pilih!"""
        
        self.add_chat_message("Maya", roleplay_message, is_bot=True)
    
    def show_help(self, instance):
        """Show help information"""
        help_text = """Panduan Maya Chatbot:

🗣️ Berbual - Taip apa sahaja dalam Bahasa Melayu
📚 Quiz - Tekan butang Quiz untuk latihan vocab
🎭 Role Play - Berlakon dalam situasi berbeza
💬 Topics - Pilih topik untuk conversation terarah

Semua topik tersedia tanpa perlu klik "More Topics":
🌟 Essential: Greetings, Food, Shopping, Transport, Family, Weather
🏠 Daily Life: Work, Hobbies, Health, School, Time, Housing  
🌍 Social: Directions, Help, Banking, Hotel, Emergency, Post Office

Contoh ayat:
- "Apa khabar?"
- "Saya lapar"  
- "Ajar saya Bahasa Melayu"

Selamat belajar! 🇸🇬"""
        
        self.add_chat_message("Maya", help_text, is_bot=True)
    
    def start_topic_conversation(self, topic):
        """Start a conversation on a specific topic"""
        topic_starters = {
            'greetings': "Selamat pagi! Apa khabar hari ini?",
            'food': "Saya lapar! Anda suka makan apa?",
            'shopping': "Mari pergi shopping! Apa yang anda nak beli?",
            'transport': "Macam mana pergi ke bandar? Naik apa?",
            'family': "Cerita tentang keluarga anda! Berapa orang?",
            'weather': "Cuaca hari ini macam mana? Panas atau hujan?",
            'work': "Apa kerja anda? Suka tak dengan kerja tu?",
            'hobbies': "Hobby anda apa? Suka main apa?",
            'health': "Kesihatan penting! Anda sihat tak?",
            'school': "Anda study apa? Sekolah mana?",
            'time': "Pukul berapa sekarang? Anda busy tak?",
            'housing': "Rumah anda di mana? Sewa atau beli?",
            'directions': "Boleh tanya jalan? Saya sesat ni!",
            'help': "Boleh tolong saya tak? Saya perlukan bantuan!",
            'banking': "Nak pergi bank! Apa urusan anda?",
            'hotel': "Selamat datang ke hotel! Ada booking?",
            'emergency': "Aduh! Emergency ni! Apa yang berlaku?",
            'postoffice': "Nak hantar surat! Berapa harga pos?"
        }
        
        starter = topic_starters.get(topic, "Mari kita berbual tentang topik ini!")
        self.add_chat_message("Maya", f"📍 {topic.title()} Topic\n\n{starter}", is_bot=True)
    
    def reset_chat(self, instance):
        """Reset the chat conversation"""
        self.chat_layout.clear_widgets()
        self.add_chat_message("Maya", "Chat direset! Selamat datang semula! Apa khabar?", is_bot=True)
    
    def show_settings_popup(self, instance):
        """Show settings popup"""
        content = BoxLayout(orientation='vertical', spacing=10)
        
        stats = self.chatbot.get_statistics()
        stats_text = f"""Statistik Maya:
        
Jumlah perbualan: {stats['total_conversations']}
Saiz vocabulary: {stats['vocabulary_size']}
Konteks semasa: {stats['context_entries']} entri

Versi: 1.0.0"""
        
        stats_label = Label(text=stats_text, halign='left')
        close_btn = Button(text='Tutup', size_hint_y=None, height='40dp')
        
        content.add_widget(stats_label)
        content.add_widget(close_btn)
        
        popup = Popup(
            title='Tetapan Maya',
            content=content,
            size_hint=(0.8, 0.6)
        )
        
        close_btn.bind(on_press=popup.dismiss)
        popup.open()

class MalayChatbotApp(App):
    def build(self):
        # Create screen manager
        sm = ScreenManager()
        
        # Add chat screen
        chat_screen = ChatScreen(name='chat')
        sm.add_widget(chat_screen)
        
        return sm

# Run the app
if __name__ == '__main__':
    MalayChatbotApp().run() 