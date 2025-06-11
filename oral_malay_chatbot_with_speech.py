#!/usr/bin/env python3
"""
Enhanced Oral Malay Chatbot with Speech Output
A friendly chatbot for practicing conversational Malay with text-to-speech capabilities.
Includes enhanced responses, context tracking, and training data integration.
"""

import random
import re
import json
import os
from datetime import datetime
from typing import Dict, List, Optional, Tuple

# Try to import speech libraries (optional)
try:
    import pyttsx3
    SPEECH_AVAILABLE = True
except ImportError:
    SPEECH_AVAILABLE = False
    print("⚠️  pyttsx3 not found. Install with: pip install pyttsx3")

try:
    import gtts
    from gtts import gTTS
    import pygame
    import tempfile
    GTTS_AVAILABLE = True
except ImportError:
    GTTS_AVAILABLE = False
    print("⚠️  gTTS not found. Install with: pip install gtts pygame")

class ContextTracker:
    """Simple context tracking for conversation flow"""
    def __init__(self):
        self.context_stack = []
        self.max_context = 5
    
    def update_context(self, user_input: str, bot_response: str):
        """Update conversation context"""
        context_entry = {
            'user': user_input,
            'bot': bot_response,
            'timestamp': datetime.now().isoformat()
        }
        self.context_stack.append(context_entry)
        
        # Keep only recent context
        if len(self.context_stack) > self.max_context:
            self.context_stack.pop(0)
    
    def get_relevant_context(self) -> List[Dict]:
        """Get recent conversation context"""
        return self.context_stack

class TrainingDataLoader:
    """Load and manage training data from JSON"""
    def __init__(self, data_file: str = "malay_training_data.json"):
        self.data_file = data_file
        self.training_data = self.load_training_data()
    
    def load_training_data(self) -> Dict:
        """Load training data from JSON file"""
        try:
            if os.path.exists(self.data_file):
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except Exception as e:
            print(f"⚠️  Could not load training data: {e}")
        
        # Return basic fallback data
        return {
            "categories": {
                "greetings": {
                    "pairs": [
                        {
                            "user_input": "hello",
                            "bot_response": "Hai! Apa khabar? Saya Maya!",
                            "english_translation": "Hi! How are you? I'm Maya!",
                            "pronunciation": "high! ah-pah kah-bar? sah-yah MY-ah!"
                        }
                    ]
                }
            }
        }

class EnhancedSpeechSystem:
    """Enhanced speech system with non-blocking TTS"""
    def __init__(self):
        self.tts_engine = None
        self.speech_enabled = False
        self.speech_available = False
        self.initialize_speech()
    
    def initialize_speech(self):
        """Initialize speech system with better error handling"""
        if SPEECH_AVAILABLE:
            try:
                self.tts_engine = pyttsx3.init()
                # Set properties for better Malay pronunciation
                self.tts_engine.setProperty('rate', 150)  # Slower for learning
                self.tts_engine.setProperty('volume', 0.8)
                self.speech_available = True
                print("✅ Speech system available (disabled by default)")
            except Exception as e:
                print(f"⚠️  Speech initialization failed: {e}")
                self.speech_available = False
        else:
            print("🔇 Speech libraries not available")
    
    def speak(self, text: str, language: str = 'malay'):
        """Non-blocking text-to-speech"""
        if not self.speech_enabled or not self.speech_available:
            return
        
        # Use threading to prevent hanging
        import threading
        
        def speak_thread():
            try:
                if self.tts_engine:
                    self.tts_engine.say(text)
                    self.tts_engine.runAndWait()
            except Exception as e:
                print(f"🔇 Speech error: {e}")
        
        try:
            # Start speech in background thread with timeout
            speech_thread = threading.Thread(target=speak_thread, daemon=True)
            speech_thread.start()
            # Don't wait for completion to avoid hanging
        except Exception as e:
            print(f"🔇 Speech thread error: {e}")

class EnhancedMalayChatbot:
    def __init__(self):
        self.name = "Maya"
        self.conversation_count = 0
        self.voice_output = False  # Disabled by default to prevent hanging
        
        # Initialize components
        self.context_tracker = ContextTracker()
        self.training_loader = TrainingDataLoader()
        self.speech_system = EnhancedSpeechSystem()
        
        # New enhanced features
        self.role_play = RolePlayScenarios()
        self.grammar_checker = GrammarChecker()
        self.vocabulary_quiz = VocabularyQuiz()
        self.current_roleplay = None
        self.quiz_mode = False
        self.current_quiz = None
        
        # Enhanced contextual features
        self.current_topic = None
        self.user_preferences = {}
        self.conversation_mood = 'neutral'
        self.last_category = None
        
        # Enhanced responses with more variety
        self.responses = {
            'greeting': [
                ("Apa khabar? Saya Maya! Siapa nama anda?", "How are you? I'm Maya! What's your name?", "ah-pah kah-bar? sah-yah MY-ah!"),
                ("Selamat datang! Bagaimana hari anda?", "Welcome! How is your day?", "seh-lah-mat dah-tang!"),
                ("Hai! Senang berjumpa dengan anda!", "Hi! Nice to meet you!", "high! seh-nang ber-joom-pah"),
                ("Assalamualaikum! Apa khabar? Sudah makan?", "Peace be upon you! How are you? Have you eaten?", "ah-sah-lah-mu-ah-lai-kum!")
            ],
            'positive': [
                ("Bagus! Saya gembira mendengarnya!", "Good! I'm happy to hear that!", "bah-goos! sah-yah gem-bee-rah"),
                ("Alhamdulillah! Itu berita yang baik!", "Praise be to God! That's good news!", "al-ham-du-lil-lah!"),
                ("Wah, bestnya! Saya suka itu!", "Wow, great! I like that!", "wah, best-nyah!"),
                ("Tahniah! Syabas kepada anda!", "Congratulations! Well done!", "tah-nee-ah! shah-bas!")
            ],
            'food': [
                ("Saya suka makan chicken rice! Anda suka apa?", "I like eating chicken rice! What do you like?", "sah-yah soo-kah mah-kan chicken rice!"),
                ("Makanan Singapore memang sedap lah!", "Singapore food is really delicious!", "mah-kah-nan sin-gah-por meh-mang seh-dap lah!"),
                ("Anda lapar ke? Jom pergi kopitiam!", "Are you hungry? Let's go to kopitiam!", "an-dah lah-par keh? jom peh-ree ko-pee-tee-ahm!"),
                ("Laksa sama bak chor mee, best lah!", "Laksa and bak chor mee, the best!", "lak-sah sah-mah bak chor mee!")
            ],
            'learning': [
                ("Bagus! Teruskan belajar bahasa Melayu!", "Good! Keep learning Malay!", "bah-goos! teh-roos-kan beh-lah-jar"),
                ("Anda dah pandai! Jangan malu untuk cuba!", "You're getting good! Don't be shy to try!", "an-dah dah pan-digh!"),
                ("Bahasa Melayu mudah sahaja. Practice makes perfect!", "Malay is easy. Practice makes perfect!", "bah-hah-sah meh-lay-oo moo-dah")
            ],
            'cultural': [
                ("Singapore truly multicultural lah! Berbagai kaum, satu negara!", "Singapore truly multicultural! Many races, one country!", "sin-gah-por truly mul-tee-cul-tu-ral lah!"),
                ("Selamat Hari Raya! Maaf zahir dan batin!", "Happy Hari Raya! Forgive me physically and spiritually!", "seh-lah-mat hah-ree rah-yah!"),
                ("Kampong spirit adalah budaya kita!", "Kampong spirit is our culture!", "kam-pong spee-rit ah-dah-lah"),
                ("Majulah Singapura! Onward Singapore!", "Majulah Singapura! Onward Singapore!", "mah-joo-lah sin-gah-poo-rah!")
            ],
            'goodbye': [
                ("Selamat tinggal! Jumpa lagi nanti!", "Goodbye! See you again later!", "seh-lah-mat ting-gal!"),
                ("Sampai jumpa! Jaga diri baik-baik!", "See you! Take good care!", "sam-pai joom-pah!"),
                ("Assalamualaikum! Allah hafez!", "Peace be upon you! May God protect you!", "ah-sah-lah-mu-ah-lai-kum!")
            ],
            'default': [
                ("Saya faham. Apa lagi yang anda nak kongsi?", "I understand. What else do you want to share?", "sah-yah fah-ham"),
                ("Menarik! Boleh cerita lebih detail?", "Interesting! Can you tell me more?", "meh-nah-rik!"),
                ("Oh begitu. Apa pendapat anda?", "Oh I see. What's your opinion?", "oh beh-gee-too"),
                ("Betul ke? Cerita lagi sikit!", "Really? Tell me more!", "beh-tool keh? cheh-ree-tah lah-gee")
            ]
        }
        
        # Enhanced keywords (Singapore-specific)
        self.keywords = {
            'greeting': ['hai', 'hello', 'hi', 'selamat', 'apa khabar', 'assalamualaikum', 'morning', 'pagi'],
            'positive': ['baik', 'bagus', 'gembira', 'senang', 'good', 'fine', 'great', 'excellent', 'best', 'shiok'],
            'food': ['makan', 'makanan', 'lapar', 'chicken rice', 'laksa', 'bak chor mee', 'kopitiam', 'hawker', 'food court', 'sedap'],
            'learning': ['belajar', 'study', 'learn', 'practice', 'bahasa', 'language', 'pandai', 'clever'],
            'cultural': ['singapore', 'singapura', 'budaya', 'culture', 'hari raya', 'festival', 'kampong', 'hdb', 'mrt'],
            'goodbye': ['bye', 'selamat tinggal', 'goodbye', 'quit', 'exit', 'jumpa lagi']
        }

    def get_response_category(self, user_input: str) -> str:
        """Enhanced response category detection"""
        if not user_input:
            return 'default'
            
        user_input_lower = user_input.lower()
        
        # Check training data first
        if self.training_loader.training_data:
            for category_name, category_data in self.training_loader.training_data.get("categories", {}).items():
                for pair in category_data.get("pairs", []):
                    if any(keyword in user_input_lower for keyword in pair.get("user_input", "").lower().split()):
                        return category_name
        
        # Check predefined keywords
        for category, keywords in self.keywords.items():
            if any(keyword in user_input_lower for keyword in keywords):
                return category
        
        return 'default'

    def analyze_user_sentiment(self, user_input: str) -> str:
        """Analyze user sentiment and emotion"""
        user_lower = user_input.lower()
        
        # Positive indicators
        if any(word in user_lower for word in ['bagus', 'best', 'shiok', 'suka', 'gembira', 'senang', 'good', 'great', 'love', 'nice']):
            return 'positive'
        
        # Negative indicators  
        elif any(word in user_lower for word in ['sedih', 'marah', 'bosan', 'sakit', 'bad', 'sad', 'angry', 'tired', 'boring']):
            return 'negative'
        
        # Question indicators
        elif any(word in user_lower for word in ['apa', 'kenapa', 'mengapa', 'mana', 'bila', 'bagaimana', 'what', 'why', 'when', 'how', 'where', '?']):
            return 'questioning'
        
        return 'neutral'
    
    def extract_keywords_and_topics(self, user_input: str) -> Dict:
        """Extract important keywords and topics from user input"""
        user_lower = user_input.lower()
        
        # Food topics
        food_keywords = ['makan', 'lapar', 'chicken rice', 'laksa', 'bak chor mee', 'kopitiam', 'hawker', 'food', 'sedap']
        # Place topics  
        place_keywords = ['singapore', 'mrt', 'orchard', 'void deck', 'hdb', 'sentosa', 'marina bay']
        # Family topics
        family_keywords = ['ibu', 'bapa', 'anak', 'adik', 'kakak', 'family', 'keluarga']
        # Activity topics
        activity_keywords = ['kerja', 'belajar', 'study', 'work', 'shopping', 'travel']
        
        detected_topics = []
        if any(word in user_lower for word in food_keywords):
            detected_topics.append('food')
        if any(word in user_lower for word in place_keywords):
            detected_topics.append('places')  
        if any(word in user_lower for word in family_keywords):
            detected_topics.append('family')
        if any(word in user_lower for word in activity_keywords):
            detected_topics.append('activities')
            
        return {
            'topics': detected_topics,
            'contains_question': '?' in user_input or any(q in user_lower for q in ['apa', 'kenapa', 'mana', 'what', 'why', 'where']),
            'mentions_singapore': 'singapore' in user_lower or 'singapura' in user_lower,
            'mentions_food': any(word in user_lower for word in food_keywords)
        }
    
    def generate_contextual_response(self, user_input: str, sentiment: str, keywords: Dict) -> Tuple[str, str, str]:
        """Generate highly contextual responses based on conversation history and analysis"""
        
        # Get conversation context
        context = self.context_tracker.get_relevant_context()
        
        # Update current topic based on keywords
        if keywords['topics']:
            self.current_topic = keywords['topics'][0]  # Use first detected topic
        
        # Handle specific contextual scenarios
        
        # 1. Follow-up responses based on conversation history
        if context and len(context) > 0:
            last_bot_response = context[-1]['bot'].lower()
            
            # If last response asked about food preferences
            if 'suka apa' in last_bot_response or 'what do you like' in last_bot_response:
                if keywords['mentions_food']:
                    return self.respond_to_food_preference(user_input)
                    
            # If last response was about Singapore places
            if any(place in last_bot_response for place in ['singapore', 'mrt', 'orchard']):
                if keywords['mentions_singapore']:
                    return self.respond_to_singapore_topic(user_input)
        
        # 2. Question handling with context
        if keywords['contains_question']:
            return self.handle_contextual_question(user_input, keywords)
        
        # 3. Sentiment-based responses
        if sentiment == 'positive':
            return self.generate_positive_response(user_input, keywords)
        elif sentiment == 'negative':
            return self.generate_supportive_response(user_input, keywords)
        
        # 4. Topic continuation
        if self.current_topic:
            return self.continue_topic_conversation(user_input, self.current_topic, keywords)
        
        # 5. Fallback to category-based with enhancement
        category = self.get_response_category(user_input)
        return self.enhance_category_response(category, user_input, keywords)
    
    def respond_to_food_preference(self, user_input: str) -> Tuple[str, str, str]:
        """Respond when user mentions food preferences"""
        responses = [
            ("Wah, sedap tu! Saya pun suka. Kat mana awak selalu makan?", "Wow, that's delicious! I like it too. Where do you usually eat?", "wah, seh-dap too!"),
            ("Eh shiok leh! Makanan Singapore memang best. Ada lagi tak yang awak suka?", "Eh that's great! Singapore food is really the best. Is there anything else you like?", "eh shiok leh!"),
            ("Betul ke? Saya pun suka tu! Kopitiam mana yang best untuk makanan tu?", "Really? I like that too! Which kopitiam is best for that food?", "beh-tool keh?")
        ]
        return random.choice(responses)
    
    def respond_to_singapore_topic(self, user_input: str) -> Tuple[str, str, str]:
        """Respond to Singapore-related topics"""
        responses = [
            ("Singapore memang lah best! Sangat convenient kan?", "Singapore is really the best! Very convenient right?", "sin-gah-por meh-mang lah best!"),
            ("Ya lor, sebab tu saya suka Singapore! Semua benda so organized.", "Yes lor, that's why I love Singapore! Everything so organized.", "ya lor!"),
            ("Betul betul! Singapore tempat yang sangat shiok untuk duduk lah!", "True true! Singapore very good place to live lah!", "betul betul!")
        ]
        return random.choice(responses)
    
    def handle_contextual_question(self, user_input: str, keywords: Dict) -> Tuple[str, str, str]:
        """Handle questions with context awareness"""
        user_lower = user_input.lower()
        
        if 'apa' in user_lower or 'what' in user_lower:
            if 'makan' in user_lower or 'food' in user_lower:
                return ("Saya recommend chicken rice lah! Sangat famous kat Singapore. Awak nak try?", "I recommend chicken rice lah! Very famous in Singapore. You want to try?", "chicken rice!")
            elif 'kerja' in user_lower or 'work' in user_lower:
                return ("Saya kerja sebagai chatbot lor! Tolong orang belajar Melayu. Awak kerja apa?", "I work as chatbot lor! Help people learn Malay. What's your job?", "sah-yah ker-jah sebagai chatbot!")
                
        elif 'mana' in user_lower or 'where' in user_lower:
            if 'makan' in user_lower:
                return ("Cuba pergi hawker centre atau kopitiam! Kat mana-mana kat Singapore ada makanan sedap.", "Try hawker centre or kopitiam! Everywhere in Singapore got good food.", "hawker centre!")
            elif 'pergi' in user_lower:
                return ("Bergantung awak nak buat apa lah! Shopping, Orchard Road. Beach, Sentosa!", "Depends what you want to do lah! Shopping, Orchard Road. Beach, Sentosa!", "ber-gan-tong awak nak!")
                
        return ("Hmm, soalan yang menarik! Cerita lagi sikit tentang apa yang awak fikir?", "Hmm, interesting question! Tell me more about what you're thinking?", "hmm, meh-nah-rik!")
    
    def generate_positive_response(self, user_input: str, keywords: Dict) -> Tuple[str, str, str]:
        """Generate enthusiastic responses to positive input"""
        responses = [
            ("Wah shiok! Saya sangat gembira dengar tu lah!", "Wah great! I'm so happy to hear that lah!", "wah shiok!"),
            ("Eh best leh! Berita yang fantastik!", "Eh best leh! That's fantastic news!", "eh best leh!"),
            ("Steady lah! Teruskan usaha!", "Steady lah! Keep it up!", "steady lah!"),
            ("Alamak bagus sangat! Saya excited untuk awak!", "Alamak so good! I'm excited for you!", "alamak bagus!")
        ]
        return random.choice(responses)
    
    def generate_supportive_response(self, user_input: str, keywords: Dict) -> Tuple[str, str, str]:
        """Generate supportive responses to negative input"""
        responses = [
            ("Aiyah, jangan risau lah! Semua akan okay.", "Aiyah, don't worry lah! Everything will be okay.", "aiyah, jangan risau!"),
            ("Haiya, takpe! Esok akan lebih baik!", "Haiya, never mind! Tomorrow will be better!", "haiya, takpe!"),
            ("Sian... tapi awak tahu tak? Boleh overcome! Saya percaya pada awak!", "Poor thing... but you know what? Can overcome! I believe in you!", "sian... tapi boleh overcome!"),
            ("Eh jangan give up! Kadang-kadang macam tu, tapi akan jadi better!", "Eh don't give up! Sometimes like that, but will get better!", "eh jangan give up!")
        ]
        return random.choice(responses)
    
    def continue_topic_conversation(self, user_input: str, topic: str, keywords: Dict) -> Tuple[str, str, str]:
        """Continue conversation on current topic"""
        if topic == 'food':
            responses = [
                ("Topik makanan sangat menarik! Apa dish Singapore yang paling awak suka?", "Food topic very interesting! What's your favorite Singapore dish?", "topik makanan!"),
                ("Eh cakap pasal makanan buat saya lapar leh! Awak dah makan ke belum?", "Eh talking about food makes me hungry leh! Have you eaten already?", "cakap pasal makanan!"),
                ("Wah budaya makanan Singapore sangat diverse kan? Ada Melayu, Cina, India...", "Wah Singapore food culture so diverse right? Got Malay, Chinese, Indian...", "budaya makanan!")
            ]
        elif topic == 'places':
            responses = [
                ("Singapore memang ada banyak tempat yang cantik! Area mana yang awak paling suka?", "Singapore really has many nice places! Which area do you like most?", "singapore memang ada!"),
                ("Setiap sudut Singapore ada benda special lah!", "Every corner of Singapore got something special lah!", "setiap sudut!"),
                ("Saya suka macam mana Singapore ni compact - semua tempat senang nak access!", "I love how compact Singapore is - everywhere so accessible!", "compact singapore!")
            ]
        else:
            responses = [
                ("Itu point yang bagus! Apa awak fikir tentang tu?", "That's a good point! What do you think about it?", "point yang bagus!"),
                ("Topik yang menarik! Boleh share lagi tentang pengalaman awak?", "Interesting topic! Can you share more about your experience?", "topik yang menarik!"),
                ("Ya lor, saya pun curious tentang tu! Cerita lagi!", "Ya lor, I'm also curious about that! Tell me more!", "ya lor curious!")
            ]
        
        return random.choice(responses)
    
    def enhance_category_response(self, category: str, user_input: str, keywords: Dict) -> Tuple[str, str, str]:
        """Enhance category responses with context"""
        # Get base response
        if category in self.responses:
            base_responses = self.responses[category]
        else:
            base_responses = self.responses['default']
        
        # Add contextual enhancement
        if keywords['mentions_singapore']:
            # Add Singapore flavor to any response
            enhanced_responses = []
            for malay, english, pronunciation in base_responses:
                if 'lah' not in malay:  # Add lah if not present
                    malay += ' lah!'
                enhanced_responses.append((malay, english, pronunciation))
            return random.choice(enhanced_responses)
        
        return random.choice(base_responses)
    
    def generate_response(self, user_input: str) -> Tuple[str, str, str]:
        """Main response generation with enhanced contextual awareness"""
        self.conversation_count += 1
        
        # First interaction is always greeting
        if self.conversation_count == 1:
            return random.choice(self.responses['greeting'])
        
        # Analyze user input
        sentiment = self.analyze_user_sentiment(user_input)
        keywords = self.extract_keywords_and_topics(user_input)
        
        # Store user preferences
        if keywords['mentions_food']:
            food_mentioned = [word for word in user_input.lower().split() if word in ['chicken rice', 'laksa', 'bak chor mee']]
            if food_mentioned:
                self.user_preferences['favorite_food'] = food_mentioned[0]
        
        # Update conversation mood
        self.conversation_mood = sentiment
        
        # Generate contextual response
        response = self.generate_contextual_response(user_input, sentiment, keywords)
        
        # Update last category for next response
        self.last_category = self.get_response_category(user_input)
        
        return response

    def speak_response(self, text: str):
        """Speak the response if voice output is enabled"""
        if self.voice_output and self.speech_system.speech_available:
            self.speech_system.speech_enabled = True
            self.speech_system.speak(text, 'malay')
        else:
            self.speech_system.speech_enabled = False
    
    def start_roleplay(self, scenario_key: str):
        """Start a role-play scenario"""
        if scenario_key in self.role_play.scenarios:
            scenario = self.role_play.scenarios[scenario_key]
            self.current_roleplay = scenario_key
            
            print(f"\n🎭 ROLE-PLAY: {scenario['title']}")
            print(f"📝 Anda adalah: {scenario['user_role']}")
            print(f"🤖 Saya adalah: {scenario['bot_role']}")
            print(f"📚 Vocabulary: {', '.join(scenario['vocabulary'])}")
            print("-" * 50)
            print(f"🤖 Maya: {scenario['starter']}")
            print("     (Type 'end roleplay' to stop)")
            self.speak_response(scenario['starter'])
            
    def handle_roleplay_response(self, user_input: str) -> str:
        """Handle responses during role-play"""
        if not self.current_roleplay:
            return None
            
        scenario = self.role_play.scenarios[self.current_roleplay]
        
        # Check if user wants to end roleplay
        if 'end roleplay' in user_input.lower():
            self.current_roleplay = None
            return "Bagus! Role-play tamat. Good! Role-play finished."
        
        # Generate contextual response based on scenario
        if self.current_roleplay == 'kopitiam':
            responses = [
                "Shiok right? Nak tambah apa lagi? Good right? Want to add anything else?",
                "Kopi or teh? Coffee or tea?",
                "Uncle recommend laksa, very sedap! Uncle recommends laksa, very delicious!",
                "Altogether $8.50 lah. Pay cash or card?",
                "Aiyah, must try our bak chor mee next time!"
            ]
        elif self.current_roleplay == 'shopping':
            responses = [
                "This one very popular, many people buy!",
                "Got discount now, 30% off leh!",
                "Size S, M, L ada. Want to try?",
                "Can pay by card or cash, up to you.",
                "Thank you ah, come again!"
            ]
        elif self.current_roleplay == 'mrt':
            responses = [
                "Take red line to City Hall, then change to green line.",
                "About 20 minutes journey lah, not far.",
                "Exit A, you will see the shopping mall.",
                "Buy EZ-link card, more convenient!",
                "No problem, welcome to Singapore!"
            ]
        elif self.current_roleplay == 'void_deck':
            responses = [
                "Wah, which unit? I stay 10th floor.",
                "This block very nice one, got playground downstairs.",
                "Weekend got market nearby, very convenient.",
                "Uncle aunty here all very friendly one!",
                "Any problem just ask lah, we all neighbors."
            ]
        else:
            responses = ["Bagus, teruskan! Good, continue!"]
            
        return random.choice(responses)
    
    def check_user_grammar(self, user_input: str):
        """Check user's grammar and provide feedback"""
        corrections = self.grammar_checker.check_grammar(user_input)
        pronunciation_tip = self.grammar_checker.get_pronunciation_tip(user_input)
        
        if corrections:
            print("\n✏️  Grammar Feedback:")
            for correction in corrections:
                print(f"   • {correction['explanation']}")
                print(f"     {correction['mistake']} → {correction['correction']}")
        
        if pronunciation_tip:
            print(f"\n🗣️  Pronunciation Tip: {pronunciation_tip}")
    
    def start_quiz(self, category: str = None):
        """Start a vocabulary quiz"""
        self.quiz_mode = True
        self.current_quiz = self.vocabulary_quiz.get_random_quiz(category)
        quiz = self.current_quiz
        
        print(f"\n🧠 VOCABULARY QUIZ - {quiz['category'].upper()}")
        print(f"❓ Apa maksud '{quiz['malay_word']}' dalam bahasa Inggeris?")
        print(f"   What does '{quiz['malay_word']}' mean in English?")
        
        for i, option in enumerate(quiz['options'], 1):
            print(f"   {i}. {option}")
        
        print("   (Type the number of your answer)")
    
    def start_themed_quiz(self, theme: str = None):
        """Start a themed cultural quiz"""
        self.quiz_mode = True
        self.current_quiz = self.vocabulary_quiz.get_themed_quiz(theme)
        quiz = self.current_quiz
        quiz['quiz_type'] = 'themed'  # Mark as themed quiz
        
        print(f"\n🎯 {quiz['title'].upper()}")
        print(f"❓ {quiz['question']}")
        
        for i, option in enumerate(quiz['options'], 1):
            print(f"   {i}. {option}")
        
        print("   (Type the number of your answer)")
    
    def handle_quiz_answer(self, user_input: str):
        """Handle quiz answers"""
        if not self.quiz_mode or not self.current_quiz:
            return
            
        try:
            answer_index = int(user_input.strip()) - 1
            quiz = self.current_quiz
            quiz_type = quiz.get('quiz_type', 'vocabulary')
            
            if quiz_type == 'themed':
                # Handle themed quiz
                if answer_index == quiz['correct_answer']:
                    print("✅ Betul! Correct!")
                    print(f"   💡 {quiz['explanation']}")
                else:
                    correct_option = quiz['options'][quiz['correct_answer']]
                    print(f"❌ Salah. Wrong.")
                    print(f"   Jawapan betul: {correct_option}")
                    print(f"   💡 {quiz['explanation']}")
            else:
                # Handle vocabulary quiz
                if answer_index == quiz['correct_index']:
                    print("✅ Betul! Correct!")
                    print(f"   {quiz['malay_word']} = {quiz['correct_answer']}")
                    
                    # Provide usage example
                    example_sentences = [
                        f"Contoh: Saya suka {quiz['malay_word']}.",
                        f"Contoh: {quiz['malay_word']} itu cantik.",
                        f"Contoh: Mana {quiz['malay_word']}?",
                    ]
                    print(f"   {random.choice(example_sentences)}")
                else:
                    print(f"❌ Salah. Wrong. Jawapan betul: {quiz['correct_answer']}")
                    print(f"   Correct answer: {quiz['malay_word']} = {quiz['correct_answer']}")
            
            self.quiz_mode = False
            self.current_quiz = None
            
        except (ValueError, IndexError):
            print("❌ Sila masukkan nombor yang betul (1-4)")
            print("   Please enter a valid number (1-4)")
    
    def show_word_of_day(self):
        """Show daily vocabulary word"""
        word = self.vocabulary_quiz.get_word_of_day()
        print(f"\n📖 WORD OF THE DAY - {word['category'].upper()}")
        print(f"🇲🇾 Malay: {word['malay']}")
        print(f"🇺🇸 English: {word['english']}")
        print(f"💬 {word['example']}")
        self.speak_response(f"Perkataan hari ini: {word['malay']}")

    def chat(self):
        """Main enhanced chat loop"""
        print("🌺 " + "="*60)
        print("   SELAMAT DATANG KE SINGAPORE MALAY CHATBOT!")
        print("   WELCOME TO SINGAPORE MALAY CHATBOT!")
        print("="*60)
        print("🤖 Maya: Hai! Saya Maya, chatbot untuk belajar bahasa Melayu Singapore!")
        print("     Hi! I'm Maya, a chatbot for learning Singapore Malay language.")
        print("     Mari kita berbual dalam bahasa Melayu Singapore lah!")
        print("     Let's chat in Singapore Malay!")
        print()
        
        # Show speech status
        if self.speech_system.speech_available:
            speech_status = "enabled" if self.voice_output else "disabled"
            print(f"✨ Features: 🔊 Text-to-speech available ({speech_status})")
        else:
            print("🔇 Text-to-speech not available")
            
        print("💡 Commands:")
        if self.speech_system.speech_available:
            print("     Type 'voice on/off' to toggle speech output")
        print("     Type 'context' to see conversation history")
        print("     Type 'help' for conversation tips")
        print("     Type 'features' to see new learning features")
        print("     Type 'quiz' to start vocabulary quiz")
        print("     Type 'roleplay' to start role-play scenarios")
        print("     Type 'word' to get word of the day")
        print("     Type 'quit' to exit")
        print("-" * 60)

        while True:
            try:
                print("\n" + "="*40)
                user_input = input("👤 Anda / You: ").strip()
                
                if not user_input:
                    print("🤖 Maya: Cakap apa-apa sahaja! Say anything!")
                    continue
                
                # Handle special commands
                if user_input.lower() == 'help':
                    print("\n📚 Tips:")
                    print("   • Talk about anything in Singapore Malay or English")
                    print("   • Ask about food, kopitiam, HDB, MRT, daily life")
                    print("   • Try: 'Apa khabar?', 'Saya lapar', 'Singapore shiok!'")
                    print("   • Mix languages naturally - it's very Singaporean!")
                    print("   • Don't worry about mistakes - practice makes perfect lah!")
                    continue
                
                if user_input.lower() == 'features':
                    print("\n🌟 NEW LEARNING FEATURES:")
                    print("🎭 SINGAPORE ROLE-PLAY SCENARIOS:")
                    print("   • kopitiam - Practice ordering at coffee shop")
                    print("   • shopping - Practice shopping at Orchard")
                    print("   • mrt - Practice asking MRT directions")
                    print("   • void_deck - Practice chatting with neighbors")
                    print("   Usage: type 'roleplay kopitiam'")
                    print("\n🧠 VOCABULARY QUIZ:")
                    print("   • keluarga (family) • makanan (singapore food)")
                    print("   • warna (colors) • masa (time) • tempat_singapore (sg places)")
                    print("   • percakapan_harian (daily conversation - common words)")
                    print("   Usage: type 'quiz' or 'quiz percakapan_harian'")
                    print("\n🎯 THEMED CULTURAL QUIZZES:")
                    print("   • hari_raya - Quiz tentang Hari Raya")
                    print("   • tahun_baru_cina - Quiz tentang Tahun Baru Cina")
                    print("   • lawatan_zoo - Quiz tentang lawatan ke zoo")
                    print("   • lawatan_muzium - Quiz tentang lawatan ke muzium")
                    print("   • hari_kebangsaan - Quiz tentang Hari Kebangsaan")
                    print("   • hari_sukan - Quiz tentang Hari Sukan")
                    print("   • medan_selera - Quiz tentang medan selera")
                    print("   Usage: type 'quiz theme' or 'quiz theme hari_raya'")
                    print("\n✏️ GRAMMAR FEEDBACK:")
                    print("   • Automatic grammar checking")
                    print("   • Pronunciation tips")
                    print("   • Just type normally and get feedback!")
                    continue
                
                if user_input.lower() == 'context':
                    context = self.context_tracker.get_relevant_context()
                    print(f"\n📋 Conversation History ({len(context)} recent messages):")
                    for i, entry in enumerate(context, 1):
                        print(f"   {i}. You: {entry['user']}")
                        print(f"      Maya: {entry['bot']}")
                    continue
                
                if user_input.lower() in ['voice on', 'voice off']:
                    if not self.speech_system.speech_available:
                        print("🔇 Speech not available. Install with: pip install pyttsx3")
                        continue
                    
                    self.voice_output = user_input.lower() == 'voice on'
                    status = "enabled" if self.voice_output else "disabled"
                    print(f"🔊 Voice output {status}")
                    continue
                
                # Handle quiz mode
                if self.quiz_mode:
                    self.handle_quiz_answer(user_input)
                    continue
                
                # Handle new commands
                if user_input.lower() == 'word':
                    self.show_word_of_day()
                    continue
                
                if user_input.lower().startswith('quiz'):
                    parts = user_input.lower().split()
                    if len(parts) > 1 and parts[1] == 'theme':
                        # Show themed quiz categories
                        themes = self.vocabulary_quiz.get_available_themes()
                        print("🎯 Available Themed Quizzes:")
                        for theme in themes:
                            title = self.vocabulary_quiz.get_theme_title(theme)
                            print(f"   • {theme} - {title}")
                        print("   Usage: quiz theme [topic] (e.g., 'quiz theme hari_raya')")
                        print("   Or type 'quiz theme' for random themed quiz")
                        continue
                    elif len(parts) > 2 and parts[1] == 'theme':
                        # Start specific themed quiz
                        theme = parts[2]
                        themes = self.vocabulary_quiz.get_available_themes()
                        if theme not in themes:
                            print(f"❌ Theme tidak wujud. Available: {', '.join(themes)}")
                            print(f"   Theme not found. Available: {', '.join(themes)}")
                            continue
                        self.start_themed_quiz(theme)
                        continue
                    else:
                        # Regular vocabulary quiz
                        category = parts[1] if len(parts) > 1 else None
                        valid_categories = ['keluarga', 'makanan', 'warna', 'masa', 'tempat_singapore', 'percakapan_harian']
                        if category and category not in valid_categories:
                            print("❌ Category tidak wujud. Available: keluarga, makanan, warna, masa, tempat_singapore, percakapan_harian")
                            print("   Category not found. Available: keluarga, makanan, warna, masa, tempat_singapore, percakapan_harian")
                            continue
                        self.start_quiz(category)
                        continue
                
                if user_input.lower().startswith('roleplay'):
                    parts = user_input.lower().split()
                    if len(parts) < 2:
                        print("🎭 Available Singapore role-plays:")
                        for key, scenario in self.role_play.scenarios.items():
                            print(f"   • {key} - {scenario['title']}")
                        print("   Usage: roleplay kopitiam")
                        continue
                    
                    scenario = parts[1]
                    if scenario not in self.role_play.scenarios:
                        print("❌ Scenario tidak wujud. Available: kopitiam, shopping, mrt, void_deck")
                        print("   Scenario not found. Available: kopitiam, shopping, mrt, void_deck")
                        continue
                    
                    self.start_roleplay(scenario)
                    continue
                
                if user_input.lower() in ['quit', 'exit', 'bye']:
                    farewell = "Terima kasih! Selamat tinggal!"
                    print(f"\n🤖 Maya: {farewell}")
                    print("     Thank you! Goodbye!")
                    self.speak_response(farewell)
                    break
                
                # Check for grammar feedback (for all user input)
                self.check_user_grammar(user_input)
                
                # Handle role-play response
                if self.current_roleplay:
                    roleplay_response = self.handle_roleplay_response(user_input)
                    if roleplay_response:
                        print(f"\n🤖 Maya: {roleplay_response}")
                        self.speak_response(roleplay_response)
                        # Update context
                        self.context_tracker.update_context(user_input, roleplay_response)
                        continue
                
                # Generate normal response
                malay_response, english_translation, pronunciation = self.generate_response(user_input)
                
                print(f"\n🤖 Maya: {malay_response}")
                print(f"     {english_translation}")
                print(f"🗣️  Pronunciation: {pronunciation}")
                
                # Speak the response (non-blocking)
                self.speak_response(malay_response)
                
                # Update context
                self.context_tracker.update_context(user_input, malay_response)
                
            except KeyboardInterrupt:
                print("\n\n🌺 Goodbye! Selamat tinggal!")
                break
            except Exception as e:
                print(f"❌ Error: {e}")
                print("   Let's continue...")
                continue

class RolePlayScenarios:
    """Role-play scenarios for conversational practice"""
    def __init__(self):
        self.scenarios = {
            'kopitiam': {
                'title': 'Di Kopitiam (At Coffee Shop)',
                'bot_role': 'uncle/auntie kopitiam (kopitiam owner)',
                'user_role': 'pelanggan (customer)',
                'starter': "Selamat datang! Nak makan apa? Chicken rice ada!",
                'vocabulary': ['chicken rice', 'laksa', 'bak chor mee', 'kopi', 'teh', 'milo', 'sedap', 'berapa', 'murah']
            },
            'shopping': {
                'title': 'Shopping di Orchard (Shopping at Orchard)',
                'bot_role': 'sales assistant',
                'user_role': 'pembeli (buyer)',
                'starter': "Good afternoon! Can I help you? Ada apa yang anda cari?",
                'vocabulary': ['beli', 'harga', 'mahal', 'murah', 'baju', 'kasut', 'beg', 'credit card', 'sale']
            },
            'mrt': {
                'title': 'Naik MRT (Taking MRT)',
                'bot_role': 'orang tempatan (local person)',
                'user_role': 'pelancong (tourist)',
                'starter': "Ya, boleh saya tolong? Nak pergi mana station?",
                'vocabulary': ['mrt', 'station', 'belok', 'kiri', 'kanan', 'dekat', 'jauh', 'interchange', 'exit']
            },
            'void_deck': {
                'title': 'Di Void Deck HDB (At HDB Void Deck)',
                'bot_role': 'jiran (neighbor)',
                'user_role': 'penduduk baru (new resident)',
                'starter': "Eh, you baru pindah ke sini? Welcome to our block!",
                'vocabulary': ['hdb', 'void deck', 'jiran', 'pindah', 'blok', 'tingkat', 'lift', 'welcome', 'kampong']
            }
        }

class GrammarChecker:
    """Simple grammar and pronunciation feedback system"""
    def __init__(self):
        self.common_corrections = {
            # Common grammar mistakes
            'saya adalah': 'saya',
            'anda adalah': 'anda',
            'dia adalah': 'dia',
            'kami adalah': 'kami',
            'mereka adalah': 'mereka',
            # Tense corrections
            'saya akan pergi kemarin': 'saya pergi kemarin',
            'saya sudah akan': 'saya akan',
            # Common word corrections
            'dimana': 'di mana',
            'kenapa': 'mengapa',
            'gimana': 'bagaimana',
        }
        
        self.pronunciation_tips = {
            'ng': 'Sebut "ng" seperti dalam "sing" - bunyi sengau',
            'ny': 'Sebut "ny" seperti dalam "canyon" - bunyi lembut',
            'kh': 'Sebut "kh" dari kerongkong, bukan "k" biasa',
            'gh': 'Sebut "gh" lembut dari kerongkong',
            'sy': 'Sebut "sy" seperti "sh" dalam bahasa Inggeris',
        }
    
    def check_grammar(self, text: str) -> List[Dict]:
        """Check for common grammar mistakes"""
        corrections = []
        text_lower = text.lower()
        
        for mistake, correction in self.common_corrections.items():
            if mistake in text_lower:
                corrections.append({
                    'type': 'grammar',
                    'mistake': mistake,
                    'correction': correction,
                    'explanation': f'Guna "{correction}" bukan "{mistake}"'
                })
        
        return corrections
    
    def get_pronunciation_tip(self, text: str) -> Optional[str]:
        """Get pronunciation tips for difficult sounds"""
        for sound, tip in self.pronunciation_tips.items():
            if sound in text.lower():
                return tip
        return None

class VocabularyQuiz:
    """Vocabulary building and quiz system"""
    def __init__(self):
        # Initialize themed quizzes
        self.themed_quizzes = {
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
            'lawatan_muzium': {
                'title': 'Quiz: Lawatan ke Muzium',
                'questions': [
                    {
                        'question': 'Di mana murid membuat lawatan?',
                        'options': ['Zoo', 'Kilang', 'Muzium', 'Hospital'],
                        'correct_answer': 2,
                        'explanation': 'Lawatan dibuat ke muzium untuk belajar sejarah.'
                    },
                    {
                        'question': 'Apa yang murid lihat di muzium?',
                        'options': ['Filem aksi', 'Baju tradisional dan barang lama', 'Haiwan', 'Tumbuhan'],
                        'correct_answer': 1,
                        'explanation': 'Muzium menyimpan baju tradisional dan artifak bersejarah.'
                    },
                    {
                        'question': 'Apa yang murid rasa tentang lawatan itu?',
                        'options': ['Menarik dan seronok', 'Membosankan', 'Menakutkan', 'Terlalu panjang'],
                        'correct_answer': 0,
                        'explanation': 'Lawatan muzium memberi pengalaman belajar yang menarik.'
                    },
                    {
                        'question': 'Apa yang cikgu suruh murid buat di muzium?',
                        'options': ['Bercakap kuat', 'Dengar penjelasan dengan baik', 'Main telefon', 'Lari-lari'],
                        'correct_answer': 1,
                        'explanation': 'Di muzium perlu dengar penjelasan dengan baik untuk belajar.'
                    }
                ]
            },
            'hari_kebangsaan': {
                'title': 'Quiz: Hari Kebangsaan',
                'questions': [
                    {
                        'question': 'Bila kita sambut Hari Kebangsaan?',
                        'options': ['1 Januari', '9 Ogos', '31 Ogos', '25 Disember'],
                        'correct_answer': 1,
                        'explanation': 'Hari Kebangsaan Malaysia disambut pada 31 Ogos setiap tahun.'
                    },
                    {
                        'question': 'Apa yang murid buat di sekolah?',
                        'options': ['Bermain', 'Tidur', 'Menyanyi lagu kebangsaan dan hormat bendera', 'Membeli makanan'],
                        'correct_answer': 2,
                        'explanation': 'Menyanyi lagu kebangsaan dan hormat bendera menunjukkan patriotisme.'
                    },
                    {
                        'question': 'Mengapa Hari Kebangsaan penting?',
                        'options': ['Dapat cuti panjang', 'Tunjuk sayang kepada negara', 'Boleh makan kek', 'Boleh tengok TV'],
                        'correct_answer': 1,
                        'explanation': 'Hari Kebangsaan penting untuk menunjukkan cinta dan patriotisme kepada negara.'
                    },
                    {
                        'question': 'Apa perasaan murid pada Hari Kebangsaan?',
                        'options': ['Sedih', 'Bangga dan gembira', 'Tak suka', 'Mengantuk'],
                        'correct_answer': 1,
                        'explanation': 'Perasaan bangga dan gembira menunjukkan semangat patriotisme.'
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
            },
            'medan_selera': {
                'title': 'Quiz: Lawatan ke Medan Selera',
                'questions': [
                    {
                        'question': 'Apa yang Imran mahu makan?',
                        'options': ['Nasi ayam', 'Mi goreng', 'Roti prata', 'Laksa'],
                        'correct_answer': 0,
                        'explanation': 'Imran mahu makan nasi ayam di medan selera.'
                    },
                    {
                        'question': 'Apa yang Rina mahu makan?',
                        'options': ['Roti canai', 'Mi goreng', 'Nasi lemak', 'Sup tulang'],
                        'correct_answer': 1,
                        'explanation': 'Rina suka mi goreng untuk makan di medan selera.'
                    },
                    {
                        'question': 'Di mana mereka duduk?',
                        'options': ['Di tangga', 'Di meja', 'Dalam kereta', 'Atas lantai'],
                        'correct_answer': 1,
                        'explanation': 'Mereka duduk di meja untuk makan dengan selesa.'
                    },
                    {
                        'question': 'Apa minuman yang Rina mahu?',
                        'options': ['Air sirap', 'Air tembikai', 'Teh tarik', 'Air limau'],
                        'correct_answer': 1,
                        'explanation': 'Rina mahu minum air tembikai yang segar.'
                    }
                ]
            }
        }
        
        # Initialize word categories
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
            'tempat_singapore': {
                'words': {
                    'kopitiam': 'coffee shop', 'void deck': 'void deck', 'hdb': 'public housing',
                    'mrt': 'mass rapid transit', 'hawker centre': 'food centre',
                    'orchard road': 'shopping street', 'marina bay': 'marina bay area', 'sentosa': 'resort island'
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
            'masa_waktu': {
                'words': {
                    'sekarang': 'now', 'tadi': 'just now', 'nanti': 'later', 'kelmarin': 'yesterday',
                    'lusa': 'day after tomorrow', 'hari': 'day', 'minggu': 'week',
                    'bulan': 'month', 'tahun': 'year', 'pagi': 'morning', 'petang': 'afternoon',
                    'malam': 'night', 'semalam': 'last night', 'esok': 'tomorrow', 'masa': 'time'
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
            'cuaca_alam': {
                'words': {
                    'hujan': 'rain', 'panorama': 'scenery', 'pantai': 'beach', 'gunung': 'mountain',
                    'pohon': 'tree', 'bunga': 'flower', 'haiwan': 'animal'
                }
            },
            'warna': {
                'words': {
                    'merah': 'red', 'biru': 'blue', 'hijau': 'green',
                    'kuning': 'yellow', 'hitam': 'black', 'putih': 'white',
                    'coklat': 'brown', 'ungu': 'purple', 'oren': 'orange'
                }
            },
            'frasa_harian': {
                'words': {
                    'apa khabar': 'how are you', 'khabar baik': 'I am fine', 'terima kasih': 'thank you',
                    'sama-sama': 'you are welcome', 'maafkan saya': 'excuse me', 'minta maaf': 'sorry',
                    'boleh saya': 'may I', 'di mana': 'where', 'berapa harga': 'how much',
                    'saya tak faham': 'I do not understand', 'tolong bantu saya': 'please help me',
                    'jumpa lagi': 'see you again', 'selamat pagi': 'good morning', 'selamat tengah hari': 'good afternoon',
                    'selamat petang': 'good evening', 'selamat malam': 'good night', 'jangan risau': 'do not worry',
                    'boleh tolong': 'can you help', 'sila masuk': 'please come in', 'tumpang tanya': 'excuse me (to ask)'
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
                    'apa lagi': 'what else', 'apakah tidak': "isn't it/don't you", 'awas': 'watch out/be careful',
                    'baiklah': 'alright/okay', 'banyak': 'many/much', 'begitu': 'like that/so',
                    'belikan': 'buy for (someone)', 'belum': 'not yet', 'benar': 'true/correct',
                    'berapa': 'how much/how many', 'bermain': 'to play', 'betul': 'correct/right',
                    'bila': 'when', 'bolehkah': 'can/may', 'bukan': "not/isn't",
                    'cuba': 'try', 'dalam': 'in/inside', 'dengan': 'with',
                    'di': 'at/in', 'dia': 'he/she/him/her', 'duitkah': 'money', 'wang': 'money',
                    'enak': 'delicious/tasty', 'lazat': 'delicious/tasty', 'faham': 'understand',
                    'kerap': 'often/frequently', 'gelap': 'dark', 'harus': 'must/should',
                    'ini': 'this', 'itu': 'that', 'jaga': 'take care/look after',
                    'jangan': "don't", 'juga': 'also/too', 'kalau': 'if',
                    'kenapa': 'why', 'khabar baik': 'fine/good news', 'kita': 'we/us',
                    'kurang': 'less/not enough', 'lagi': 'more/again', 'maafkan saya': 'forgive me/excuse me',
                    'mahu': 'want', 'mana': 'which/where', 'mari': "come/let's",
                    'mereka': 'they/them', 'misalnya': 'for example', 'muda': 'young',
                    'nampak': 'see/look', 'pukul': "hit/o'clock", 'saja': 'only/just',
                    'sana': 'there', 'sedikit': 'a little/few', 'sehaja': 'only/just',
                    'sekarang': 'now', 'senang': 'easy/happy', 'siapa': 'who',
                    'sila': 'please', 'silakan': 'please', 'sini': 'here',
                    'sudah': 'already/finished', 'sudikah': 'would you/are you willing', 'susah': 'difficult/hard',
                    'tahu': 'know', 'tahukah': 'do you know', 'tak banyak': 'not much/not many',
                    'tapi': 'but', 'tetapi': 'but', 'tentu boleh': 'of course/certainly can',
                    'tidak cukup': 'not enough', 'tidak mengapa': "it's okay/never mind", 'tidak usah': 'no need',
                    'untuk awak': 'for you', 'yang': 'which/that', 'sebelah': 'beside/next to'
                }
            }
        }
    
    def get_random_quiz(self, category: str = None) -> Dict:
        """Generate a random vocabulary quiz"""
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
    
    def get_word_of_day(self) -> Dict:
        """Get a daily vocabulary word"""
        category = random.choice(list(self.word_categories.keys()))
        words = self.word_categories[category]['words']
        malay_word = random.choice(list(words.keys()))
        
        return {
            'category': category,
            'malay': malay_word,
            'english': words[malay_word],
            'example': f"Contoh: Saya suka {malay_word}. (Example: I like {words[malay_word]}.)"
        }
    
    def get_themed_quiz(self, theme: str = None) -> Dict:
        """Get a themed cultural quiz"""
        if theme and theme in self.themed_quizzes:
            selected_theme = theme
        else:
            selected_theme = random.choice(list(self.themed_quizzes.keys()))
        
        quiz_data = self.themed_quizzes[selected_theme]
        question = random.choice(quiz_data['questions'])
        
        return {
            'theme': selected_theme,
            'title': quiz_data['title'],
            'question': question['question'],
            'options': question['options'],
            'correct_answer': question['correct_answer'],
            'explanation': question['explanation']
        }
    
    def get_available_themes(self) -> List[str]:
        """Get list of available themed quiz topics"""
        return list(self.themed_quizzes.keys())
    
    def get_theme_title(self, theme: str) -> str:
        """Get the display title for a theme"""
        if theme in self.themed_quizzes:
            return self.themed_quizzes[theme]['title']
        return theme

def main():
    """Main function"""
    print("🚀 Starting Singapore Malay Chatbot...")
    chatbot = EnhancedMalayChatbot()
    chatbot.chat()

if __name__ == "__main__":
    main() 