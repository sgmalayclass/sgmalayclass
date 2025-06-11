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
# ActionBar imports removed - using regular buttons instead
from kivy.clock import Clock
from kivy.core.audio import SoundLoader
from kivy.utils import get_color_from_hex

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

class MalayChatbotCore:
    """Core chatbot logic - adapted from the original chatbot"""
    def __init__(self):
        self.name = "Maya"
        self.conversation_count = 0
        self.context_stack = []
        self.max_context = 5
        self.current_topic = None
        self.quiz_mode = False
        self.current_quiz = None
        self.current_roleplay = None
        
        # Initialize vocabulary database
        self.word_categories = {
            'keluarga': {
                'words': {
                    'ibu': 'mother', 'bapa': 'father', 'anak': 'child',
                    'adik': 'younger sibling', 'abang': 'older brother',
                    'kakak': 'older sister', 'nenek': 'grandmother',
                    'datuk': 'grandfather', 'sepupu': 'cousin', 'keluarga': 'family',
                    'tetangga': 'neighbor'
                }
            },
            'makanan': {
                'words': {
                    'chicken rice': 'chicken rice', 'laksa': 'spicy noodle soup', 'bak chor mee': 'minced meat noodles',
                    'char kway teow': 'fried flat noodles', 'satay': 'grilled meat skewers', 'rojak': 'mixed fruit salad',
                    'kopi': 'coffee', 'teh': 'tea', 'milo': 'chocolate drink', 'nasi lemak': 'coconut rice dish',
                    'roti': 'bread', 'teh tarik': 'pulled tea', 'susu': 'milk', 'aiskrim': 'ice cream',
                    'makanan': 'food', 'minuman': 'drink', 'pedas': 'spicy', 'manis': 'sweet',
                    'makan malam': 'dinner', 'sedap': 'delicious'
                }
            },
            'tempat': {
                'words': {
                    'rumah': 'house', 'sekolah': 'school', 'taman': 'park', 'taman permainan': 'playground',
                    'perpustakaan': 'library', 'kantin sekolah': 'school canteen', 'pasar': 'market',
                    'bilik': 'room', 'dapur': 'kitchen', 'tandas': 'toilet', 'muzium': 'museum',
                    'tempat': 'place', 'jalan': 'road/street'
                }
            },
            'aktiviti': {
                'words': {
                    'membaca buku': 'reading books', 'melukis gambar': 'drawing pictures', 'bermain bola': 'playing ball',
                    'membantu ibu': 'helping mother', 'membasuh pinggan': 'washing dishes', 'main': 'play',
                    'baca': 'read', 'tulis': 'write', 'masak': 'cook', 'cuci': 'wash',
                    'bersihkan': 'clean', 'kerja rumah': 'homework'
                }
            },
            'festival_budaya': {
                'words': {
                    'Hari Raya': 'Eid celebration', 'Tahun Baru Cina': 'Chinese New Year', 'angpao': 'red packet',
                    'kuih raya': 'Eid cookies', 'baju kurung': 'traditional Malay dress', 'pakaian tradisional': 'traditional clothing',
                    'Hari Kebangsaan': 'National Day', 'lawatan sekolah': 'school trip', 'haiwan liar': 'wild animals'
                }
            },
            'taman_permainan': {
                'words': {
                    'gelongsor': 'slide', 'buaian': 'swing', 'jongkang-jongkit': 'seesaw',
                    'tolak': 'push', 'kuat-kuat': 'strongly', 'hati-hati': 'be careful'
                }
            },
            'kata_kerja': {
                'words': {
                    'makan': 'eat', 'minum': 'drink', 'pergi': 'go', 'datang': 'come',
                    'lihat': 'see', 'tengok': 'look', 'suka': 'like', 'main': 'play',
                    'cakap': 'speak', 'berkata': 'say', 'duduk': 'sit', 'bangun': 'wake up/stand up',
                    'ambil': 'take', 'beri': 'give', 'tidur': 'sleep', 'baca': 'read',
                    'tulis': 'write', 'beli': 'buy', 'jual': 'sell', 'buka': 'open',
                    'tutup': 'close', 'dengar': 'hear', 'tunggu': 'wait', 'buat': 'make/do',
                    'pandu': 'drive', 'ajar': 'teach', 'faham': 'understand', 'masak': 'cook',
                    'cuci': 'wash', 'bersihkan': 'clean', 'hantar': 'send', 'terima': 'receive',
                    'simpan': 'keep', 'cari': 'search', 'jumpa': 'meet'
                }
            },
            'kata_nama': {
                'words': {
                    'rumah': 'house', 'sekolah': 'school', 'kawan': 'friend', 'rakan': 'friend',
                    'makanan': 'food', 'minuman': 'drink', 'taman': 'park', 'keluarga': 'family',
                    'kerja rumah': 'homework', 'bilik': 'room', 'kasut': 'shoes', 'air': 'water',
                    'kereta': 'car', 'duit': 'money', 'orang': 'person', 'masa': 'time',
                    'hari': 'day', 'tangan': 'hand', 'mata': 'eye', 'jalan': 'road',
                    'pasar': 'market', 'doktor': 'doctor', 'tempat': 'place', 'rak': 'shelf'
                }
            },
            'pengangkutan': {
                'words': {
                    'bas': 'bus', 'teksi': 'taxi', 'stesen': 'station', 'tiket': 'ticket',
                    'peta': 'map', 'kereta': 'car', 'mrt': 'MRT'
                }
            },
            'kata_sifat': {
                'words': {
                    'baik': 'good', 'buruk': 'bad', 'besar': 'big', 'kecil': 'small',
                    'cantik': 'beautiful', 'panas': 'hot', 'sejuk': 'cold', 'cepat': 'fast',
                    'lambat': 'slow', 'sedap': 'delicious', 'rajin': 'diligent', 'malas': 'lazy',
                    'mahal': 'expensive', 'murah': 'cheap', 'lama': 'long/old', 'baru': 'new'
                }
            },
            'perasaan': {
                'words': {
                    'gembira': 'happy', 'sedih': 'sad', 'marah': 'angry', 'lapar': 'hungry',
                    'haus': 'thirsty', 'penat': 'tired', 'sibuk': 'busy'
                }
            },
            'frasa_harian': {
                'words': {
                    'apa khabar': 'how are you', 'khabar baik': 'I am fine', 'terima kasih': 'thank you',
                    'sama-sama': 'you are welcome', 'maafkan saya': 'excuse me', 'minta maaf': 'sorry',
                    'boleh saya': 'may I', 'di mana': 'where', 'berapa harga': 'how much',
                    'saya tak faham': 'I do not understand', 'tolong bantu saya': 'please help me',
                    'jumpa lagi': 'see you again', 'selamat pagi': 'good morning', 'selamat tengah hari': 'good afternoon',
                    'selamat petang': 'good evening', 'selamat malam': 'good night', 'jangan risau': 'do not worry'
                }
            },
            'beli_belah': {
                'words': {
                    'ada diskaun': 'is there discount', 'boleh kurang sikit': 'can reduce a little',
                    'saya cuma melihat': 'I am just looking', 'tunai': 'cash', 'kad kredit': 'credit card',
                    'saiz ini terlalu besar': 'this size is too big', 'saiz ini terlalu kecil': 'this size is too small',
                    'bungkuskan ya': 'please wrap it', 'harga': 'price', 'beli': 'buy'
                }
            },
            'percakapan_harian': {
                'words': {
                    'akan': 'will/going to', 'apa': 'what', 'apa khabar': 'how are you',
                    'apa lagi': 'what else', 'apakah tidak': "isn't it/don't you",
                    'baiklah': 'alright/okay', 'banyak': 'many/much', 'begitu': 'like that/so',
                    'belum': 'not yet', 'benar': 'true/correct', 'betul': 'correct/right',
                    'bila': 'when', 'bolehkah': 'can/may', 'bukan': "not/isn't",
                    'cuba': 'try', 'dalam': 'in/inside', 'dengan': 'with',
                    'di': 'at/in', 'dia': 'he/she/him/her', 'faham': 'understand',
                    'ini': 'this', 'itu': 'that', 'jaga': 'take care',
                    'kenapa': 'why', 'kita': 'we/us', 'mahu': 'want',
                    'mari': "come/let's", 'sekarang': 'now', 'senang': 'easy/happy',
                    'siapa': 'who', 'sila': 'please', 'sudah': 'already',
                    'tahu': 'know', 'tapi': 'but', 'yang': 'which/that', 'sebelah': 'beside/next to'
                }
            }
        }
        
        # Response patterns
        self.responses = {
            'greeting': [
                ("Apa khabar? Saya Maya! Siapa nama anda?", "How are you? I'm Maya! What's your name?"),
                ("Selamat datang! Bagaimana hari anda?", "Welcome! How is your day?"),
                ("Hai! Senang berjumpa dengan anda!", "Hi! Nice to meet you!")
            ],
            'positive': [
                ("Bagus! Saya gembira mendengarnya!", "Good! I'm happy to hear that!"),
                ("Wah, bestnya! Saya suka itu!", "Wow, great! I like that!"),
                ("Tahniah! Syabas kepada anda!", "Congratulations! Well done!")
            ],
            'food': [
                ("Saya suka chicken rice! Anda suka apa?", "I like chicken rice! What do you like?"),
                ("Makanan Singapore memang sedap lah!", "Singapore food is really delicious!"),
                ("Anda lapar ke? Jom pergi kopitiam!", "Are you hungry? Let's go to kopitiam!")
            ],
            'default': [
                ("Saya faham. Apa lagi yang anda nak kongsi?", "I understand. What else do you want to share?"),
                ("Menarik! Boleh cerita lebih detail?", "Interesting! Can you tell me more?"),
                ("Betul ke? Cerita lagi sikit!", "Really? Tell me more!")
            ]
        }
        
        # Keywords for response categorization
        self.keywords = {
            'greeting': ['hai', 'hello', 'hi', 'selamat', 'apa khabar'],
            'positive': ['baik', 'bagus', 'gembira', 'senang', 'good', 'great', 'best'],
            'food': ['makan', 'makanan', 'lapar', 'chicken rice', 'laksa', 'sedap'],
            'goodbye': ['bye', 'selamat tinggal', 'goodbye', 'quit', 'exit']
        }
        
        # Role-play scenarios
        self.roleplay_scenarios = {
            'kopitiam': {
                'title': 'Di Kopitiam (At Coffee Shop)',
                'starter': "Selamat datang! Nak makan apa? Chicken rice ada!"
            },
            'shopping': {
                'title': 'Shopping di Orchard (Shopping at Orchard)',
                'starter': "Good afternoon! Can I help you? Ada apa yang anda cari?"
            }
        }
    
    def update_context(self, user_input: str, bot_response: str):
        """Update conversation context"""
        self.context_stack.append({
            'user': user_input,
            'bot': bot_response,
            'timestamp': datetime.now().isoformat()
        })
        if len(self.context_stack) > self.max_context:
            self.context_stack.pop(0)
    
    def get_response_category(self, user_input: str) -> str:
        """Determine response category based on keywords"""
        user_lower = user_input.lower()
        for category, keywords in self.keywords.items():
            if any(keyword in user_lower for keyword in keywords):
                return category
        return 'default'
    
    def generate_response(self, user_input: str) -> Tuple[str, str]:
        """Generate chatbot response"""
        self.conversation_count += 1
        
        if self.conversation_count == 1:
            response = random.choice(self.responses['greeting'])
            return response[0], response[1]
        
        category = self.get_response_category(user_input)
        if category in self.responses:
            response = random.choice(self.responses[category])
        else:
            response = random.choice(self.responses['default'])
        
        return response[0], response[1]
    
    def generate_quiz(self, category: str = None) -> Dict:
        """Generate vocabulary quiz"""
        if category and category in self.word_categories:
            selected_category = category
        else:
            selected_category = random.choice(list(self.word_categories.keys()))
        
        words = self.word_categories[selected_category]['words']
        malay_word = random.choice(list(words.keys()))
        english_word = words[malay_word]
        
        # Create multiple choice options
        all_english = list(words.values())
        wrong_options = [word for word in all_english if word != english_word]
        options = [english_word] + random.sample(wrong_options, min(3, len(wrong_options)))
        random.shuffle(options)
        
        return {
            'category': selected_category,
            'malay_word': malay_word,
            'correct_answer': english_word,
            'options': options,
            'correct_index': options.index(english_word)
        }
    
    def generate_themed_quiz(self, theme: str = None) -> Dict:
        """Generate a themed cultural quiz"""
        themed_quizzes = {
            'hari_raya': {
                'title': 'Quiz: Hari Raya',
                'questions': [
                    {
                        'question': 'Apa yang Hana pakai semasa Hari Raya?',
                        'options': ['Baju T-shirt', 'Baju kurung baru', 'Seluar pendek', 'Baju sekolah'],
                        'correct_answer': 1,
                        'explanation': 'Baju kurung adalah pakaian tradisional yang dipakai semasa Hari Raya.'
                    },
                    {
                        'question': 'Siapa datang melawat rumah Hana?',
                        'options': ['Guru sekolah', 'Pak cik dan mak cik', 'Polis', 'Jiran sebelah'],
                        'correct_answer': 1,
                        'explanation': 'Pak cik dan mak cik datang melawat untuk beraya bersama-sama.'
                    },
                    {
                        'question': 'Apa yang Hana dan keluarga makan?',
                        'options': ['Pizza', 'Ketupat dan rendang', 'Mi goreng', 'Nasi lemak'],
                        'correct_answer': 1,
                        'explanation': 'Ketupat dan rendang adalah makanan tradisional Hari Raya.'
                    },
                    {
                        'question': 'Apa maksud Hari Raya bagi Hana?',
                        'options': ['Masa untuk bersama keluarga dan memohon maaf', 'Hari membeli-belah', 'Hari main permainan', 'Hari cuti belajar'],
                        'correct_answer': 0,
                        'explanation': 'Hari Raya adalah masa untuk bersama keluarga dan saling memohon maaf.'
                    }
                ]
            },
            'tahun_baru_cina': {
                'title': 'Quiz: Tahun Baru Cina',
                'questions': [
                    {
                        'question': 'Apakah warna pakaian Wei Ming pada Tahun Baru Cina?',
                        'options': ['Biru', 'Merah', 'Putih', 'Hitam'],
                        'correct_answer': 1,
                        'explanation': 'Warna merah melambangkan keberuntungan dalam budaya Cina.'
                    },
                    {
                        'question': 'Apakah makanan yang dimakan oleh Wei Ming dan keluarganya?',
                        'options': ['Burger', 'Satay', 'Makan besar', 'Kek coklat'],
                        'correct_answer': 2,
                        'explanation': 'Makan besar atau reunion dinner adalah tradisi penting Tahun Baru Cina.'
                    },
                    {
                        'question': 'Apa yang mereka lakukan selepas makan besar?',
                        'options': ['Membakar bunga api', 'Menonton televisyen', 'Pergi ke sekolah', 'Tidur'],
                        'correct_answer': 0,
                        'explanation': 'Membakar bunga api adalah aktiviti tradisional Tahun Baru Cina.'
                    },
                    {
                        'question': 'Apa yang Wei Ming rasa tentang Tahun Baru Cina?',
                        'options': ['Seronok kerana dapat angpao dan masa bersama keluarga', 'Penat dan bosan', 'Tak suka makanan', 'Rindu sekolah'],
                        'correct_answer': 0,
                        'explanation': 'Tahun Baru Cina adalah masa gembira untuk dapat angpao dan berkumpul keluarga.'
                    }
                ]
            },
            'lawatan_zoo': {
                'title': 'Quiz: Lawatan ke Zoo',
                'questions': [
                    {
                        'question': 'Apa tujuan lawatan ke zoo?',
                        'options': ['Bermain bola', 'Melihat haiwan liar', 'Menyanyi', 'Bercuti'],
                        'correct_answer': 1,
                        'explanation': 'Tujuan lawatan ke zoo adalah untuk melihat dan belajar tentang haiwan liar.'
                    },
                    {
                        'question': 'Bagaimana murid pergi ke zoo?',
                        'options': ['Naik MRT', 'Naik bas sekolah', 'Naik kereta api', 'Jalan kaki'],
                        'correct_answer': 1,
                        'explanation': 'Lawatan sekolah biasanya menggunakan bas sekolah.'
                    },
                    {
                        'question': 'Apakah haiwan yang paling disukai murid?',
                        'options': ['Harimau', 'Singa', 'Zirafah', 'Ular'],
                        'correct_answer': 2,
                        'explanation': 'Zirafah popular kerana lehernya yang panjang dan perangai yang lembut.'
                    },
                    {
                        'question': 'Apa yang cikgu pesan kepada murid?',
                        'options': ['Jangan beri makan kepada haiwan', 'Ambil gambar haiwan dengan lampu', 'Balik awal', 'Tidur di zoo'],
                        'correct_answer': 0,
                        'explanation': 'Jangan beri makan haiwan untuk keselamatan haiwan dan pengunjung.'
                    }
                ]
            },
            'hari_sukan': {
                'title': 'Quiz: Hari Sukan',
                'questions': [
                    {
                        'question': 'Acara apa yang Siti sertai?',
                        'options': ['Lompat jauh', 'Larian 100 meter', 'Bola sepak', 'Tarik tali'],
                        'correct_answer': 1,
                        'explanation': 'Siti sertai acara larian 100 meter pada Hari Sukan.'
                    },
                    {
                        'question': 'Apa acara Ahmad?',
                        'options': ['Lari pecut', 'Lompat jauh', 'Lontar peluru', 'Bola jaring'],
                        'correct_answer': 1,
                        'explanation': 'Ahmad menyertai acara lompat jauh.'
                    },
                    {
                        'question': 'Apa nasihat Ahmad kepada Siti?',
                        'options': ['Minum air banyak', 'Tidur awal', 'Bawa makanan', 'Ambil gambar'],
                        'correct_answer': 0,
                        'explanation': 'Minum air banyak penting untuk elak dehidrasi semasa sukan.'
                    },
                    {
                        'question': 'Apa cuaca semasa Hari Sukan?',
                        'options': ['Hujan', 'Panas', 'Sejuk', 'Berangin'],
                        'correct_answer': 1,
                        'explanation': 'Cuaca panas memerlukan lebih banyak minum air.'
                    }
                ]
            }
        }
        
        if not theme or theme not in themed_quizzes:
            theme = random.choice(list(themed_quizzes.keys()))
        
        quiz_data = themed_quizzes[theme]
        question = random.choice(quiz_data['questions'])
        
        return {
            'theme': theme,
            'title': quiz_data['title'],
            'question': question['question'],
            'options': question['options'],
            'correct_answer': question['correct_answer'],
            'explanation': question['explanation'],
            'quiz_type': 'themed'
        }

class ChatScreen(Screen):
    """Main chat interface screen"""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.chatbot = MalayChatbotCore()
        self.build_interface()
    
    def build_interface(self):
        """Build the chat interface"""
        # Main layout
        main_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # Header with title and menu
        header_layout = BoxLayout(orientation='horizontal', size_hint_y=0.08, 
                                spacing=10, padding=[10, 5])
        
        # Title
        title_label = Label(
            text='🤖 Maya - Malay Chatbot',
            color=get_color_from_hex('#FFFFFF'),
            size_hint_x=0.6,
            text_size=(None, None)
        )
        
        # Menu buttons
        quiz_btn = Button(
            text='Quiz',
            size_hint_x=0.2,
            background_color=get_color_from_hex('#2196F3')
        )
        quiz_btn.bind(on_press=self.show_quiz_menu)
        
        roleplay_btn = Button(
            text='Role-play',
            size_hint_x=0.2,
            background_color=get_color_from_hex('#FF9800')
        )
        roleplay_btn.bind(on_press=self.show_roleplay_menu)
        
        header_layout.add_widget(title_label)
        header_layout.add_widget(quiz_btn)
        header_layout.add_widget(roleplay_btn)
        
        # Chat history area
        self.chat_scroll = ScrollView()
        self.chat_layout = GridLayout(cols=1, spacing=10, size_hint_y=None)
        self.chat_layout.bind(minimum_height=self.chat_layout.setter('height'))
        self.chat_scroll.add_widget(self.chat_layout)
        
        # Input area
        input_layout = BoxLayout(orientation='horizontal', size_hint_y=0.1, spacing=10)
        
        self.text_input = TextInput(
            hint_text='Type your message in Malay or English...',
            multiline=False,
            size_hint_x=0.8
        )
        self.text_input.bind(on_text_validate=self.send_message)
        
        send_btn = Button(
            text='Send',
            size_hint_x=0.2,
            background_color=get_color_from_hex('#4CAF50')
        )
        send_btn.bind(on_press=self.send_message)
        
        input_layout.add_widget(self.text_input)
        input_layout.add_widget(send_btn)
        
        # Add all components to main layout
        main_layout.add_widget(header_layout)
        main_layout.add_widget(self.chat_scroll)
        main_layout.add_widget(input_layout)
        
        self.add_widget(main_layout)
        
        # Add welcome message
        self.add_chat_message("Maya", 
                             "Hai! Saya Maya! Mari belajar bahasa Melayu bersama!\nHi! I'm Maya! Let's learn Malay together!",
                             is_bot=True)
    
    def add_chat_message(self, sender: str, message: str, is_bot: bool = False):
        """Add a message to the chat interface"""
        # Create message bubble
        message_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=60)
        
        if is_bot:
            # Bot message (left aligned, blue)
            message_label = Label(
                text=f"🤖 {sender}: {message}",
                text_size=(300, None),
                halign='left',
                valign='middle',
                color=get_color_from_hex('#2196F3'),
                size_hint_x=0.8
            )
            message_layout.add_widget(message_label)
            message_layout.add_widget(Label(size_hint_x=0.2))  # Spacer
        else:
            # User message (right aligned, green)
            message_layout.add_widget(Label(size_hint_x=0.2))  # Spacer
            message_label = Label(
                text=f"👤 {sender}: {message}",
                text_size=(300, None),
                halign='right',
                valign='middle',
                color=get_color_from_hex('#4CAF50'),
                size_hint_x=0.8
            )
            message_layout.add_widget(message_label)
        
        self.chat_layout.add_widget(message_layout)
        
        # Auto-scroll to bottom
        Clock.schedule_once(lambda dt: setattr(self.chat_scroll, 'scroll_y', 0), 0.1)
    
    def send_message(self, instance=None):
        """Handle sending messages"""
        user_message = self.text_input.text.strip()
        if not user_message:
            return
        
        # Add user message to chat
        self.add_chat_message("You", user_message, is_bot=False)
        
        # Generate bot response
        malay_response, english_translation = self.chatbot.generate_response(user_message)
        bot_message = f"{malay_response}\n{english_translation}"
        
        # Add bot response to chat
        self.add_chat_message("Maya", bot_message, is_bot=True)
        
        # Update context
        self.chatbot.update_context(user_message, malay_response)
        
        # Clear input
        self.text_input.text = ""
    
    def show_quiz_menu(self, instance):
        """Show quiz category selection"""
        popup_layout = BoxLayout(orientation='vertical', spacing=10)
        
        popup_layout.add_widget(Label(text='Choose Quiz Category:', size_hint_y=0.2))
        
        categories = ['keluarga', 'makanan', 'percakapan_harian', 'random']
        for category in categories:
            btn = Button(text=category.title(), size_hint_y=0.2)
            btn.bind(on_press=lambda x, cat=category: self.start_quiz(cat))
            popup_layout.add_widget(btn)
        
        popup = Popup(title='Vocabulary Quiz', content=popup_layout, size_hint=(0.8, 0.6))
        popup.open()
        
        # Store popup reference to close it later
        self.quiz_popup = popup
    
    def start_quiz(self, category):
        """Start a vocabulary quiz"""
        self.quiz_popup.dismiss()
        
        quiz_category = None if category == 'random' else category
        quiz = self.chatbot.generate_quiz(quiz_category)
        
        # Create quiz interface
        quiz_layout = BoxLayout(orientation='vertical', spacing=10)
        
        quiz_layout.add_widget(Label(
            text=f"Quiz: {quiz['category'].title()}\n\nApa maksud '{quiz['malay_word']}'?",
            size_hint_y=0.3
        ))
        
        # Answer buttons
        for i, option in enumerate(quiz['options']):
            btn = Button(text=f"{i+1}. {option}", size_hint_y=0.15)
            btn.bind(on_press=lambda x, idx=i, q=quiz: self.check_quiz_answer(idx, q))
            quiz_layout.add_widget(btn)
        
        popup = Popup(title='Vocabulary Quiz', content=quiz_layout, size_hint=(0.9, 0.8))
        popup.open()
        self.current_quiz_popup = popup
    
    def check_quiz_answer(self, selected_index, quiz):
        """Check quiz answer and show result"""
        self.current_quiz_popup.dismiss()
        
        if selected_index == quiz['correct_index']:
            result_text = f"✅ Betul! Correct!\n\n{quiz['malay_word']} = {quiz['correct_answer']}"
        else:
            result_text = f"❌ Salah. Wrong.\n\nJawapan betul: {quiz['correct_answer']}"
        
        result_popup = Popup(
            title='Quiz Result',
            content=Label(text=result_text),
            size_hint=(0.8, 0.4)
        )
        result_popup.open()
        
        # Auto-close after 3 seconds
        Clock.schedule_once(lambda dt: result_popup.dismiss(), 3)
    
    def show_roleplay_menu(self, instance):
        """Show role-play scenario selection"""
        popup_layout = BoxLayout(orientation='vertical', spacing=10)
        
        popup_layout.add_widget(Label(text='Choose Role-play Scenario:', size_hint_y=0.3))
        
        for key, scenario in self.chatbot.roleplay_scenarios.items():
            btn = Button(text=scenario['title'], size_hint_y=0.35)
            btn.bind(on_press=lambda x, k=key: self.start_roleplay(k))
            popup_layout.add_widget(btn)
        
        popup = Popup(title='Role-play Scenarios', content=popup_layout, size_hint=(0.8, 0.5))
        popup.open()
        self.roleplay_popup = popup
    
    def start_roleplay(self, scenario_key):
        """Start a role-play scenario"""
        self.roleplay_popup.dismiss()
        
        scenario = self.chatbot.roleplay_scenarios[scenario_key]
        self.chatbot.current_roleplay = scenario_key
        
        # Add role-play message
        roleplay_msg = f"🎭 ROLE-PLAY: {scenario['title']}\n\n{scenario['starter']}"
        self.add_chat_message("Maya", roleplay_msg, is_bot=True)

class MalayChatbotApp(App):
    """Main application class"""
    def build(self):
        self.title = 'Maya - Malay Learning Chatbot'
        
        # Create screen manager
        sm = ScreenManager()
        
        # Add main chat screen
        chat_screen = ChatScreen(name='chat')
        sm.add_widget(chat_screen)
        
        return sm

# Run the app
if __name__ == '__main__':
    MalayChatbotApp().run() 