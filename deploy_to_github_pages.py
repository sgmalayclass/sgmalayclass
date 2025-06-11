#!/usr/bin/env python3
"""
🚀 Deploy Maya Chatbot to GitHub Pages
Creates a permanent website URL for your chatbot
"""

import os
import shutil
import subprocess

def deploy_to_github():
    print("🚀 GitHub Pages Deployment for Maya Chatbot")
    print("=" * 50)
    
    # Check if git is available
    try:
        subprocess.run(['git', '--version'], check=True, capture_output=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ Git not found. Please install Git first:")
        print("   https://git-scm.com/download/win")
        return
    
    print("📋 STEP-BY-STEP INSTRUCTIONS:")
    print()
    
    print("1️⃣ Create GitHub Repository:")
    print("   • Go to github.com and create new repository")
    print("   • Name it: maya-chatbot")
    print("   • Make it PUBLIC")
    print("   • Don't initialize with README")
    print()
    
    print("2️⃣ Upload Your Files:")
    print("   • Clone your new repository:")
    print("     git clone https://github.com/YOUR_USERNAME/maya-chatbot.git")
    print("   • Copy maya_chatbot_webapp.html to the repository folder")
    print("   • Rename it to: index.html")
    print()
    
    print("3️⃣ Push to GitHub:")
    print("     cd maya-chatbot")
    print("     git add index.html")
    print('     git commit -m "Add Maya Chatbot"')
    print("     git push origin main")
    print()
    
    print("4️⃣ Enable GitHub Pages:")
    print("   • Go to repository Settings")
    print("   • Scroll to Pages section")
    print("   • Source: Deploy from a branch")
    print("   • Branch: main")
    print("   • Folder: / (root)")
    print("   • Click Save")
    print()
    
    print("5️⃣ Your Website Will Be At:")
    print("   https://YOUR_USERNAME.github.io/maya-chatbot/")
    print()
    
    # Create index.html from existing webapp
    if os.path.exists('maya_chatbot_webapp.html'):
        shutil.copy2('maya_chatbot_webapp.html', 'index.html')
        print("✅ Created index.html (ready for GitHub Pages)")
        print("📁 File: index.html")
    else:
        print("❌ maya_chatbot_webapp.html not found")
    
    print()
    print("🌟 BENEFITS:")
    print("   ✅ Permanent URL")
    print("   ✅ Works on cellular data")
    print("   ✅ No file size limits")
    print("   ✅ Professional domain")
    print("   ✅ Free forever")

if __name__ == "__main__":
    deploy_to_github() 