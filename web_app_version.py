#!/usr/bin/env python3
"""
Maya Malay Chatbot - Web App Version
A web-based version that works on all mobile devices through browsers.
Can be installed as a Progressive Web App (PWA).
"""

from flask import Flask, render_template, request, jsonify
import random
import json
import os
from datetime import datetime

app = Flask(__name__)

class MalayChatbotWeb:
    """Web version of the Malay chatbot"""
    def __init__(self):
        self.name = "Maya"
        self.conversation_count = 0
        self.context_stack = []
        self.max_context = 5
        
        # Vocabulary database - same as mobile app
        self.word_categories = {
            'keluarga': {
                'words': {
                    'ibu': 'mother', 'bapa': 'father', 'anak': 'child',
                    'adik': 'younger sibling', 'abang': 'older brother',
                    'kakak': 'older sister', 'nenek': 'grandmother',
                    'datuk': 'grandfather', 'sepupu': 'cousin'
                }
            },
            'makanan': {
                'words': {
                    'chicken rice': 'chicken rice', 'laksa': 'spicy noodle soup', 
                    'bak chor mee': 'minced meat noodles', 'char kway teow': 'fried flat noodles',
                    'satay': 'grilled meat skewers', 'rojak': 'mixed fruit salad',
                    'kopi': 'coffee', 'teh': 'tea', 'milo': 'chocolate drink'
                }
            },
            'percakapan_harian': {
                'words': {
                    'akan': 'will/going to', 'apa': 'what', 'apa khabar': 'how are you',
                    'apa lagi': 'what else', 'baiklah': 'alright/okay', 'banyak': 'many/much',
                    'begitu': 'like that/so', 'belum': 'not yet', 'benar': 'true/correct',
                    'betul': 'correct/right', 'bila': 'when', 'bolehkah': 'can/may',
                    'bukan': "not/isn't", 'cuba': 'try', 'dalam': 'in/inside',
                    'dengan': 'with', 'di': 'at/in', 'dia': 'he/she/him/her',
                    'faham': 'understand', 'ini': 'this', 'itu': 'that',
                    'jaga': 'take care', 'kenapa': 'why', 'kita': 'we/us',
                    'mahu': 'want', 'mari': "come/let's", 'sekarang': 'now',
                    'senang': 'easy/happy', 'siapa': 'who', 'sila': 'please',
                    'sudah': 'already', 'tahu': 'know', 'tapi': 'but', 'yang': 'which/that'
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
        
        # Keywords for response detection
        self.keywords = {
            'greeting': ['hai', 'hello', 'hi', 'selamat', 'apa khabar'],
            'positive': ['baik', 'bagus', 'gembira', 'senang', 'good', 'great', 'best'],
            'food': ['makan', 'makanan', 'lapar', 'chicken rice', 'laksa', 'sedap'],
            'goodbye': ['bye', 'selamat tinggal', 'goodbye']
        }
    
    def get_response_category(self, user_input):
        """Determine response category"""
        user_lower = user_input.lower()
        for category, keywords in self.keywords.items():
            if any(keyword in user_lower for keyword in keywords):
                return category
        return 'default'
    
    def generate_response(self, user_input):
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
        
        # Update context
        self.context_stack.append({
            'user': user_input,
            'bot': response[0],
            'timestamp': datetime.now().isoformat()
        })
        if len(self.context_stack) > self.max_context:
            self.context_stack.pop(0)
        
        return response[0], response[1]
    
    def generate_quiz(self, category=None):
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

# Initialize chatbot
chatbot = MalayChatbotWeb()

@app.route('/')
def index():
    """Main page"""
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    """Handle chat messages"""
    user_message = request.json.get('message', '')
    malay_response, english_translation = chatbot.generate_response(user_message)
    
    return jsonify({
        'malay': malay_response,
        'english': english_translation,
        'status': 'success'
    })

@app.route('/quiz/<category>')
def quiz(category=None):
    """Generate quiz"""
    quiz_data = chatbot.generate_quiz(category if category != 'random' else None)
    return jsonify(quiz_data)

@app.route('/quiz/check', methods=['POST'])
def check_quiz():
    """Check quiz answer"""
    selected_index = request.json.get('selected_index')
    correct_index = request.json.get('correct_index')
    correct_answer = request.json.get('correct_answer')
    
    is_correct = selected_index == correct_index
    return jsonify({
        'correct': is_correct,
        'answer': correct_answer,
        'message': '✅ Betul! Correct!' if is_correct else '❌ Salah. Wrong.'
    })

if __name__ == '__main__':
    # Create templates directory if it doesn't exist
    if not os.path.exists('templates'):
        os.makedirs('templates')
    
    # Create static directory for CSS/JS
    if not os.path.exists('static'):
        os.makedirs('static')
    
    print("🌐 Starting Maya Malay Chatbot Web App...")
    print("📱 Access on mobile: http://your-ip:5000")
    print("💻 Access locally: http://localhost:5000")
    app.run(host='0.0.0.0', port=5000, debug=True) 