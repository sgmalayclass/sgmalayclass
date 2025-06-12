#!/usr/bin/env python3
"""
Maya Chatbot - Simplified Command Line Version
Efficient implementation using the unified chatbot core.
"""

import sys
import os
from chatbot_core import MalayChatbotCore

def print_welcome():
    """Print welcome message"""
    print("=" * 60)
    print("🇸🇬 MAYA - CHATBOT BAHASA MELAYU SINGAPORE 🇸🇬")
    print("=" * 60)
    print("Selamat datang! Mari belajar Bahasa Melayu!")
    print("Welcome! Let's learn Malay together!")
    print()
    print("Commands:")
    print("  'quiz' - Start vocabulary quiz")
    print("  'stats' - Show statistics")
    print("  'topics' - Show all conversation topics") 
    print("  'help' - Show this help")
    print("  'exit' or 'bye' - Exit chatbot")
    print()
    print("💬 All Conversation Topics Available:")
    print("🌟 Essential: greetings, food, shopping, transport, family, weather")
    print("🏠 Daily Life: work, hobbies, health, school, time, housing")
    print("🌍 Social: directions, help, banking, hotel, emergency")
    print("💼 Professional: jobinterview, postoffice, cultural")
    print("💡 Tip: Type any topic name to start that conversation!")
    print("-" * 60)

def main():
    """Main chat loop"""
    # Initialize chatbot
    try:
        chatbot = MalayChatbotCore()
        print("✅ Maya chatbot initialized successfully!")
    except Exception as e:
        print(f"❌ Error initializing chatbot: {e}")
        return
    
    print_welcome()
    
    while True:
        try:
            # Get user input
            user_input = input("\n👤 You: ").strip()
            
            if not user_input:
                continue
            
            # Handle special commands
            if user_input.lower() in ['exit', 'quit', 'bye', 'selamat tinggal']:
                print("\n🤖 Maya: Selamat tinggal! Jumpa lagi! 👋")
                print("🤖 Maya: Goodbye! See you again! 👋")
                break
            
            elif user_input.lower() == 'quiz':
                # Start quiz mode
                quiz = chatbot.generate_quiz()
                if quiz:
                    print(f"\n📚 QUIZ: {quiz['question']}")
                    for i, option in enumerate(quiz['options'], 1):
                        print(f"  {i}. {option}")
                    
                    try:
                        answer = input("\nPilih jawapan (1-4): ").strip()
                        answer_idx = int(answer) - 1
                        
                        if 0 <= answer_idx < len(quiz['options']):
                            selected_answer = quiz['options'][answer_idx]
                            if selected_answer == quiz['correct_answer']:
                                print("✅ Betul! Correct!")
                            else:
                                print(f"❌ Salah. Jawapan betul: {quiz['correct_answer']}")
                        else:
                            print("❌ Nombor tidak sah. Invalid number.")
                    except (ValueError, IndexError):
                        print("❌ Sila masukkan nombor 1-4. Please enter number 1-4.")
                else:
                    print("❌ Quiz tidak tersedia. Quiz not available.")
                continue
            
            elif user_input.lower() == 'stats':
                # Show statistics
                stats = chatbot.get_statistics()
                print("\n📊 STATISTIK MAYA:")
                print(f"  Jumlah perbualan: {stats['total_conversations']}")
                print(f"  Saiz vocabulary: {stats['vocabulary_size']}")
                print(f"  Konteks semasa: {stats['context_entries']} entri")
                print(f"  Topik semasa: {stats['current_topic'] or 'Tiada'}")
                continue
            
            elif user_input.lower() == 'topics':
                # Show all available topics
                print("\n💬 ALL CONVERSATION TOPICS:")
                print("=" * 50)
                print("🌟 ESSENTIAL TOPICS:")
                print("  • greetings - Basic hello and introductions")
                print("  • food - Singapore/Malaysian cuisine discussion")
                print("  • shopping - Market, mall, and bargaining")
                print("  • transport - MRT, bus, taxi conversations")
                print("  • family - Family members and relationships")
                print("  • weather - Weather and climate chat")
                print()
                print("🏠 DAILY LIFE TOPICS:")
                print("  • work - Job and career discussions")
                print("  • hobbies - Sports, interests, and activities")
                print("  • health - Medical and wellness topics")
                print("  • school - Education and learning")
                print("  • time - Clock time and scheduling")
                print("  • housing - Home and accommodation")
                print()
                print("🌍 SOCIAL & TRAVEL TOPICS:")
                print("  • directions - Asking for and giving directions")
                print("  • help - Requesting assistance")
                print("  • banking - Bank services and transactions")
                print("  • hotel - Hotel booking and services")
                print("  • emergency - Emergency situations")
                print("  • postoffice - Mail and postal services")
                print()
                print("💼 PROFESSIONAL TOPICS:")
                print("  • jobinterview - Job interview practice")
                print("  • cultural - Cultural events and festivals")
                print()
                print("💡 HOW TO USE: Just type any topic name to start!")
                print("📝 Example: Type 'food' to start food conversations")
                continue
            
            elif user_input.lower() == 'help':
                print_welcome()
                continue
            
            # Generate response
            malay_response, english_translation = chatbot.generate_response(user_input)
            
            # Display response
            print(f"\n🤖 Maya: {malay_response}")
            print(f"         ({english_translation})")
            
            # Update context
            chatbot.update_context(user_input, malay_response)
            
        except KeyboardInterrupt:
            print("\n\n🤖 Maya: Terima kasih! Thank you! 👋")
            break
        except Exception as e:
            print(f"❌ Error: {e}")
            print("Sila cuba lagi. Please try again.")

if __name__ == "__main__":
    main() 