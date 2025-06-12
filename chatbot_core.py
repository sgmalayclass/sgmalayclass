#!/usr/bin/env python3
"""
Unified Malay Chatbot Core
Consolidates all chatbot functionality into a single, efficient implementation.
"""

import json
import random
import re
import os
from datetime import datetime
from typing import Dict, List, Optional, Tuple
import threading
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MalayChatbotCore:
    """
    Unified chatbot core with optimized performance and consolidated functionality.
    """
    
    def __init__(self, training_data_file: str = "malay_training_data.json"):
        self.name = "Maya"
        self.conversation_count = 0
        self.context_stack = []
        self.max_context = 5
        self.current_topic = None
        self.quiz_mode = False
        self.current_quiz = None
        self.user_preferences = {}
        
        # Load training data efficiently
        self.training_data = self._load_training_data(training_data_file)
        self.vocabulary = self._extract_vocabulary()
        
        # Initialize response patterns
        self._init_response_patterns()
        
        # Performance optimization
        self._compiled_patterns = self._compile_regex_patterns()
    
    def _load_training_data(self, file_path: str) -> Dict:
        """Load and validate training data."""
        try:
            if os.path.exists(file_path):
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                logger.info(f"Loaded training data from {file_path}")
                return data
        except Exception as e:
            logger.warning(f"Could not load training data: {e}")
        
        # Return optimized fallback data
        return self._get_fallback_data()
    
    def _get_fallback_data(self) -> Dict:
        """Return streamlined fallback training data."""
        return {
            "categories": {
                "greetings": {
                    "patterns": ["apa khabar", "hello", "hi", "selamat"],
                    "responses": [
                        ("Apa khabar? Saya Maya! Siapa nama anda?", "How are you? I'm Maya! What's your name?"),
                        ("Selamat datang! Bagaimana hari anda?", "Welcome! How is your day?"),
                        ("Hai! Senang berjumpa dengan anda!", "Hi! Nice to meet you!")
                    ]
                },
                "food": {
                    "patterns": ["makan", "lapar", "makanan", "chicken rice", "nasi lemak"],
                    "responses": [
                        ("Saya suka chicken rice! Anda suka apa?", "I like chicken rice! What do you like?"),
                        ("Makanan Singapore memang sedap lah!", "Singapore food is really delicious!"),
                        ("Anda lapar ke? Jom pergi kopitiam!", "Are you hungry? Let's go to kopitiam!")
                    ]
                },
                "goodbye": {
                    "patterns": ["bye", "sampai jumpa", "selamat tinggal"],
                    "responses": [
                        ("Selamat tinggal! Jumpa lagi nanti!", "Goodbye! See you again later!"),
                        ("Sampai jumpa! Jaga diri baik-baik!", "See you! Take good care!")
                    ]
                }
            }
        }
    
    def _extract_vocabulary(self) -> Dict[str, str]:
        """Extract vocabulary from training data for quick lookup."""
        vocab = {}
        try:
            for category_data in self.training_data.get("categories", {}).values():
                if "vocabulary" in category_data:
                    vocab.update(category_data["vocabulary"])
        except Exception as e:
            logger.warning(f"Error extracting vocabulary: {e}")
        return vocab
    
    def _init_response_patterns(self):
        """Initialize optimized response patterns."""
        self.sentiment_keywords = {
            'positive': ['bagus', 'best', 'suka', 'gembira', 'senang', 'good', 'great'],
            'negative': ['tak suka', 'buruk', 'sedih', 'bad', 'terrible'],
            'question': ['apa', 'mana', 'macam mana', 'bila', 'siapa', 'kenapa']
        }
        
        self.topic_keywords = {
            'food': ['makan', 'makanan', 'lapar', 'sedap', 'chicken rice', 'nasi lemak'],
            'location': ['rumah', 'sekolah', 'singapore', 'tempat', 'di mana'],
            'family': ['ibu', 'bapa', 'anak', 'keluarga', 'adik', 'abang'],
            'learning': ['belajar', 'ajar', 'sekolah', 'buku', 'bahasa']
        }
    
    def _compile_regex_patterns(self) -> Dict:
        """Pre-compile regex patterns for better performance."""
        patterns = {}
        try:
            for category, keywords in self.topic_keywords.items():
                pattern = r'\b(?:' + '|'.join(re.escape(kw) for kw in keywords) + r')\b'
                patterns[category] = re.compile(pattern, re.IGNORECASE)
        except Exception as e:
            logger.error(f"Error compiling regex patterns: {e}")
        return patterns
    
    def detect_intent(self, user_input: str) -> Tuple[str, float]:
        """Efficiently detect user intent with confidence score."""
        user_input_lower = user_input.lower()
        best_category = "default"
        best_score = 0.0
        
        # Use compiled patterns for fast matching
        for category, pattern in self._compiled_patterns.items():
            matches = pattern.findall(user_input_lower)
            if matches:
                score = len(matches) / len(user_input.split())
                if score > best_score:
                    best_score = score
                    best_category = category
        
        # Check for greeting patterns
        greeting_words = ['hello', 'hi', 'apa khabar', 'selamat']
        if any(word in user_input_lower for word in greeting_words):
            return "greeting", 0.8
        
        # Check for goodbye patterns
        goodbye_words = ['bye', 'sampai jumpa', 'selamat tinggal']
        if any(word in user_input_lower for word in goodbye_words):
            return "goodbye", 0.8
        
        return best_category, best_score
    
    def generate_response(self, user_input: str) -> Tuple[str, str]:
        """Generate contextual response efficiently."""
        try:
            # Detect intent
            intent, confidence = self.detect_intent(user_input)
            
            # Get appropriate response
            if intent in self.training_data.get("categories", {}):
                responses = self.training_data["categories"][intent].get("responses", [])
                if responses:
                    malay_response, english_translation = random.choice(responses)
                    return malay_response, english_translation
            
            # Fallback responses
            fallback_responses = [
                ("Saya faham. Apa lagi yang anda nak kongsi?", "I understand. What else do you want to share?"),
                ("Menarik! Boleh cerita lebih detail?", "Interesting! Can you tell me more?"),
                ("Oh begitu. Apa pendapat anda?", "Oh I see. What's your opinion?")
            ]
            
            return random.choice(fallback_responses)
            
        except Exception as e:
            logger.error(f"Error generating response: {e}")
            return ("Maaf, saya tidak faham. Boleh ulang?", "Sorry, I don't understand. Can you repeat?")
    
    def update_context(self, user_input: str, bot_response: str):
        """Update conversation context efficiently."""
        context_entry = {
            'user': user_input,
            'bot': bot_response,
            'timestamp': datetime.now().isoformat(),
            'turn': self.conversation_count
        }
        
        self.context_stack.append(context_entry)
        
        # Keep only recent context for memory efficiency
        if len(self.context_stack) > self.max_context:
            self.context_stack.pop(0)
        
        self.conversation_count += 1
    
    def get_context_summary(self) -> str:
        """Get a summary of recent conversation context."""
        if not self.context_stack:
            return "No context available"
        
        recent_topics = []
        for entry in self.context_stack[-3:]:
            intent, _ = self.detect_intent(entry['user'])
            if intent != "default":
                recent_topics.append(intent)
        
        if recent_topics:
            return f"Recent topics: {', '.join(set(recent_topics))}"
        return "General conversation"
    
    def generate_quiz(self, category: str = None) -> Optional[Dict]:
        """Generate vocabulary quiz efficiently."""
        if not self.vocabulary:
            return None
        
        try:
            # Select random words for quiz
            vocab_items = list(self.vocabulary.items())
            if len(vocab_items) < 4:
                return None
            
            # Select correct answer
            correct_word, correct_meaning = random.choice(vocab_items)
            
            # Generate distractors
            distractors = random.sample(
                [meaning for word, meaning in vocab_items if word != correct_word], 
                min(3, len(vocab_items) - 1)
            )
            
            # Create options
            options = [correct_meaning] + distractors
            random.shuffle(options)
            
            return {
                'question': f"Apa maksud '{correct_word}' dalam Bahasa Inggeris?",
                'options': options,
                'correct_answer': correct_meaning,
                'category': category or 'general'
            }
            
        except Exception as e:
            logger.error(f"Error generating quiz: {e}")
            return None
    
    def is_quiz_mode(self) -> bool:
        """Check if currently in quiz mode."""
        return self.quiz_mode
    
    def start_quiz_mode(self):
        """Start quiz mode."""
        self.quiz_mode = True
        self.current_quiz = self.generate_quiz()
    
    def end_quiz_mode(self):
        """End quiz mode."""
        self.quiz_mode = False
        self.current_quiz = None
    
    def get_statistics(self) -> Dict:
        """Get chatbot usage statistics."""
        return {
            'total_conversations': self.conversation_count,
            'context_entries': len(self.context_stack),
            'vocabulary_size': len(self.vocabulary),
            'current_topic': self.current_topic,
            'quiz_mode': self.quiz_mode
        } 