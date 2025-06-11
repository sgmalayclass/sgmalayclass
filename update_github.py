#!/usr/bin/env python3
"""
GitHub Repository Update Script for Maya Chatbot Melayu v2.0
This script helps you update your GitHub repository with the latest features
"""

import os
import subprocess
import sys
from pathlib import Path

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"📝 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"❌ Error in {description}: {e}")
        print(f"Command output: {e.stdout}")
        print(f"Command error: {e.stderr}")
        return None

def check_git_status():
    """Check if we're in a git repository"""
    if not os.path.exists('.git'):
        print("❌ This directory is not a git repository!")
        print("Please run: git init")
        return False
    return True

def main():
    """Main deployment function"""
    print("🚀 Maya Chatbot Melayu v2.0 - GitHub Update Script")
    print("=" * 60)
    
    # Check if we're in a git repository
    if not check_git_status():
        return
    
    # List of files to commit
    files_to_commit = [
        "oral_malay_chatbot_with_speech.py",
        "malay_chatbot_mobile_app.py", 
        "malay_training_data.json",
        "updated_malay_vocabulary_complete.csv",
        "malay_vocabulary_organized.csv",
        "index_updated.html",
        "README_Updated.md",
        "requirements.txt",
        "maya_chatbot_melayu_v1.0.0.apk",
        "maya_chatbot_working_v1.0.0.apk"
    ]
    
    print("📋 Files to be updated:")
    for file in files_to_commit:
        if os.path.exists(file):
            print(f"   ✅ {file}")
        else:
            print(f"   ❌ {file} (not found)")
    
    # Check git status
    run_command("git status", "Checking git status")
    
    # Add files
    print("\n📤 Adding files to git...")
    for file in files_to_commit:
        if os.path.exists(file):
            run_command(f"git add {file}", f"Adding {file}")
    
    # Add any new files
    run_command("git add .", "Adding all new files")
    
    # Commit changes
    commit_message = """🎉 Maya Chatbot v2.0 - Major Update

✨ New Features:
- 🎯 Themed Cultural Quizzes (7 themes, 28 questions)
- 📚 Expanded Vocabulary Database (400+ words)
- 🎮 Enhanced Role-Play Scenarios
- 📱 Mobile App with APK distribution
- 🗣️ Improved Speech & Audio Features
- 📊 Complete Word Type Analysis (Verbs, Nouns, Adjectives)

🔧 Technical Improvements:
- Enhanced conversation AI
- Better grammar checking
- Pronunciation guides
- Progress tracking
- Cultural learning integration

📱 Deployment:
- Updated web interface
- Mobile APK ready for distribution
- GitHub Pages compatibility
- Comprehensive documentation

🎓 Educational Content:
- Singapore/Malaysian cultural context
- Real-world conversation practice
- Systematic vocabulary building
- Interactive learning experience"""

    run_command(f'git commit -m "{commit_message}"', "Committing changes")
    
    # Push to GitHub
    print("\n🚀 Pushing to GitHub...")
    result = run_command("git push origin main", "Pushing to main branch")
    
    if result is None:
        # Try master branch if main doesn't work
        run_command("git push origin master", "Pushing to master branch")
    
    print("\n🎉 GitHub Repository Update Complete!")
    print("\n📋 Next Steps:")
    print("1. 🌐 Enable GitHub Pages in repository settings")
    print("2. 📱 Create a release for the APK file")
    print("3. 🔗 Update repository description and topics")
    print("4. 📝 Consider creating a GitHub Pages custom domain")
    
    print("\n🔗 Suggested Repository Topics:")
    topics = [
        "malay-language", "language-learning", "chatbot", "ai", 
        "singapore", "malaysia", "education", "mobile-app", 
        "cultural-learning", "vocabulary", "speech-recognition",
        "text-to-speech", "interactive-learning", "kivy", "python"
    ]
    print("   " + ", ".join(topics))
    
    print("\n📖 GitHub Pages Setup:")
    print("1. Go to your repository settings")
    print("2. Scroll to 'Pages' section") 
    print("3. Select 'Deploy from a branch'")
    print("4. Choose 'main' branch and '/ (root)' folder")
    print("5. Save and wait for deployment")
    print("6. Your site will be available at: https://yourusername.github.io/repository-name")
    
    print("\n🏷️ Creating a Release:")
    print("1. Go to your repository main page")
    print("2. Click 'Releases' on the right sidebar")
    print("3. Click 'Create a new release'")
    print("4. Tag version: v2.0.0")
    print("5. Release title: 'Maya Chatbot Melayu v2.0 - Cultural Learning Update'")
    print("6. Upload the APK file as a release asset")
    print("7. Publish the release")

if __name__ == "__main__":
    main() 