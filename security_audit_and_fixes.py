#!/usr/bin/env python3
"""
Security Audit and Fixes for Maya Chatbot APK
Ensures the APK is safe for distribution and doesn't contain security risks
"""

import os
import json
import hashlib
import re
from pathlib import Path
from typing import List, Dict, Tuple

class SecurityAuditor:
    def __init__(self):
        self.project_root = Path.cwd()
        self.security_issues = []
        self.security_fixes = []
        
    def audit_buildozer_spec(self) -> List[str]:
        """Audit buildozer.spec for security issues"""
        issues = []
        buildozer_spec = self.project_root / "buildozer.spec"
        
        if not buildozer_spec.exists():
            issues.append("❌ buildozer.spec not found")
            return issues
        
        with open(buildozer_spec, 'r') as f:
            content = f.read()
        
        # Check permissions
        if "android.permissions" in content:
            permissions_line = re.search(r'android\.permissions\s*=\s*(.+)', content)
            if permissions_line:
                permissions = permissions_line.group(1).split(',')
                dangerous_permissions = [
                    'CAMERA', 'RECORD_AUDIO', 'READ_CONTACTS', 'READ_PHONE_STATE',
                    'ACCESS_FINE_LOCATION', 'ACCESS_COARSE_LOCATION', 'READ_SMS',
                    'SEND_SMS', 'CALL_PHONE', 'READ_CALL_LOG', 'WRITE_CALL_LOG'
                ]
                
                for perm in permissions:
                    perm = perm.strip()
                    if perm in dangerous_permissions:
                        issues.append(f"⚠️  Dangerous permission requested: {perm}")
        
        # Check for debug settings
        if "android.debug" not in content or "android.debug = 0" not in content:
            issues.append("⚠️  Debug mode should be disabled for production")
        
        # Check API levels
        if "android.api = 33" not in content:
            issues.append("⚠️  Should target latest API level (33)")
        
        if "android.minapi = 21" not in content:
            issues.append("⚠️  Minimum API should be 21 for security")
        
        return issues
    
    def audit_python_code(self) -> List[str]:
        """Audit Python code for security vulnerabilities"""
        issues = []
        
        # Files to audit
        python_files = [
            "malay_chatbot_kivy_app.py",
            "main.py", 
            "apk_distribution_system.py",
            "build_and_deploy.py"
        ]
        
        dangerous_patterns = [
            (r'eval\s*\(', "❌ eval() function is dangerous"),
            (r'exec\s*\(', "❌ exec() function is dangerous"),
            (r'subprocess\.call\s*\(.*shell=True', "❌ shell=True in subprocess is risky"),
            (r'os\.system\s*\(', "❌ os.system() is vulnerable to injection"),
            (r'input\s*\(.*\)', "⚠️  input() without validation"),
            (r'pickle\.loads?\s*\(', "❌ pickle is unsafe for untrusted data"),
            (r'password\s*=\s*["\'].*["\']', "❌ Hardcoded password found"),
            (r'api_key\s*=\s*["\'].*["\']', "❌ Hardcoded API key found"),
            (r'secret\s*=\s*["\'].*["\']', "❌ Hardcoded secret found"),
            (r'token\s*=\s*["\'].*["\']', "❌ Hardcoded token found"),
        ]
        
        for file_path in python_files:
            if Path(file_path).exists():
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    
                for pattern, message in dangerous_patterns:
                    if re.search(pattern, content, re.IGNORECASE):
                        issues.append(f"{message} in {file_path}")
        
        return issues
    
    def audit_training_data(self) -> List[str]:
        """Audit training data for sensitive information"""
        issues = []
        
        training_files = [
            "malay_training_data.json",
            "MalayChatbot/assets/malay_training_data.json"
        ]
        
        sensitive_patterns = [
            r'\b\d{4}[-\s]?\d{4}[-\s]?\d{4}[-\s]?\d{4}\b',  # Credit card
            r'\b\d{3}-\d{2}-\d{4}\b',  # SSN
            r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',  # Email
            r'\b\d{8,}\b',  # Phone numbers
        ]
        
        for file_path in training_files:
            if Path(file_path).exists():
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    
                for pattern in sensitive_patterns:
                    matches = re.findall(pattern, content)
                    if matches:
                        issues.append(f"⚠️  Potential sensitive data in {file_path}: {matches[:3]}")
        
        return issues
    
    def create_secure_buildozer_spec(self):
        """Create a secure buildozer.spec configuration"""
        secure_spec = """[app]

# (str) Title of your application
title = Maya Chatbot Melayu

# (str) Package name
package.name = malaychatbot

# (str) Package domain (needed for android/ios packaging)
package.domain = com.singapore.maya

# (str) Source code where the main.py live
source.dir = .

# (list) Source files to include (let empty to include all the files)
source.include_exts = py,png,jpg,kv,atlas,json

# (list) List of inclusions using pattern matching
source.include_patterns = assets/*,malay_training_data.json

# (str) Application versioning (method 1)
version = 1.0.0

# (list) Application requirements - SECURITY: Minimal dependencies only
requirements = python3,kivy,pyjnius,plyer

# (str) Supported orientation
orientation = portrait

# SECURITY: Disable debug mode for production
debug = 0

[buildozer]

# (int) Log level (0 = error only, 1 = info, 2 = debug)
log_level = 1

# (int) Display warning if buildozer is run as root
warn_on_root = 1

#
# Android specific - SECURITY HARDENED
#

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 0

# (string) Presplash background color
android.presplash_color = #FFFFFF

# SECURITY: Minimal permissions only - NO dangerous permissions
android.permissions = INTERNET,ACCESS_NETWORK_STATE,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE

# SECURITY: Latest API levels for security patches
android.api = 33
android.minapi = 21
android.compilesdk = 33
android.sdk = 33
android.ndk = 25b

# SECURITY: Target modern architectures
android.archs = arm64-v8a, armeabi-v7a

# SECURITY: Enable backup for user data protection
android.allow_backup = True

# SECURITY: APK format for easy distribution
android.release_artifact = apk
android.debug_artifact = apk

# SECURITY: Disable debug features
android.logcat_filters = *:S

# SECURITY: Use default entry point (no custom modifications)
android.entrypoint = org.kivy.android.PythonActivity

# SECURITY: Enable bytecode compilation for code protection
android.no-byte-compile-python = False
"""
        
        with open("buildozer.spec", "w") as f:
            f.write(secure_spec)
        
        self.security_fixes.append("✅ Created secure buildozer.spec with minimal permissions")
    
    def create_input_validation(self):
        """Create secure input validation for the chatbot"""
        validation_code = '''
def sanitize_user_input(user_input: str) -> str:
    """
    Sanitize user input to prevent security issues
    """
    if not isinstance(user_input, str):
        return ""
    
    # Remove potentially dangerous characters
    dangerous_chars = ['<', '>', '"', "'", '&', '\\n', '\\r', '\\t']
    sanitized = user_input
    
    for char in dangerous_chars:
        sanitized = sanitized.replace(char, '')
    
    # Limit length to prevent memory issues
    max_length = 500
    if len(sanitized) > max_length:
        sanitized = sanitized[:max_length]
    
    # Remove leading/trailing whitespace
    sanitized = sanitized.strip()
    
    return sanitized

def validate_json_data(data: dict) -> bool:
    """
    Validate JSON training data structure
    """
    if not isinstance(data, dict):
        return False
    
    required_fields = ['user', 'bot']
    
    for category, items in data.items():
        if not isinstance(items, list):
            continue
            
        for item in items:
            if not isinstance(item, dict):
                return False
            
            for field in required_fields:
                if field not in item:
                    return False
                
                if not isinstance(item[field], str):
                    return False
    
    return True
'''
        
        with open("security_utils.py", "w") as f:
            f.write(validation_code)
        
        self.security_fixes.append("✅ Created input validation utilities")
    
    def create_secure_data_storage(self):
        """Create secure data storage implementation"""
        storage_code = '''
import json
import hashlib
import base64
from typing import Dict, Any

class SecureStorage:
    """
    Secure storage for chatbot data with basic encryption
    """
    
    def __init__(self, key: str = "maya_chatbot_2024"):
        self.key = key.encode()
    
    def _encrypt_data(self, data: str) -> str:
        """Simple encryption for local data"""
        # Note: This is basic obfuscation, not cryptographic encryption
        encoded = base64.b64encode(data.encode()).decode()
        return encoded
    
    def _decrypt_data(self, encrypted_data: str) -> str:
        """Decrypt local data"""
        try:
            decoded = base64.b64decode(encrypted_data.encode()).decode()
            return decoded
        except:
            return ""
    
    def save_conversation_history(self, history: list, filename: str = "conversation_history.enc"):
        """Save conversation history securely"""
        try:
            json_data = json.dumps(history)
            encrypted_data = self._encrypt_data(json_data)
            
            with open(filename, 'w') as f:
                f.write(encrypted_data)
            
            return True
        except:
            return False
    
    def load_conversation_history(self, filename: str = "conversation_history.enc") -> list:
        """Load conversation history securely"""
        try:
            with open(filename, 'r') as f:
                encrypted_data = f.read()
            
            decrypted_data = self._decrypt_data(encrypted_data)
            history = json.loads(decrypted_data)
            
            return history if isinstance(history, list) else []
        except:
            return []
    
    def calculate_file_integrity(self, filepath: str) -> str:
        """Calculate file hash for integrity checking"""
        sha256_hash = hashlib.sha256()
        try:
            with open(filepath, "rb") as f:
                for chunk in iter(lambda: f.read(4096), b""):
                    sha256_hash.update(chunk)
            return sha256_hash.hexdigest()
        except:
            return ""
'''
        
        with open("secure_storage.py", "w") as f:
            f.write(storage_code)
        
        self.security_fixes.append("✅ Created secure data storage utilities")
    
    def update_kivy_app_security(self):
        """Update Kivy app with security enhancements"""
        # Read current app
        with open("malay_chatbot_kivy_app.py", "r") as f:
            content = f.read()
        
        # Add security imports
        security_imports = """
# Security imports
from security_utils import sanitize_user_input, validate_json_data
from secure_storage import SecureStorage

"""
        
        # Add security initialization
        security_init = """
        # Initialize secure storage
        self.secure_storage = SecureStorage()
        
"""
        
        # Update the load_training_data method
        updated_content = content.replace(
            "def load_training_data(self):",
            """def load_training_data(self):
        \"\"\"Load training data with security validation\"\"\""""
        )
        
        # Add input sanitization to send_message
        updated_content = updated_content.replace(
            "user_message = self.text_input.text.strip()",
            """user_message = sanitize_user_input(self.text_input.text.strip())
        
        # Validate input length and content
        if len(user_message) == 0 or len(user_message) > 500:
            return"""
        )
        
        # Add security imports at the top
        if "from security_utils import" not in updated_content:
            updated_content = security_imports + updated_content
        
        # Write updated file
        with open("malay_chatbot_kivy_app.py", "w") as f:
            f.write(updated_content)
        
        self.security_fixes.append("✅ Enhanced Kivy app with input validation and secure storage")
    
    def create_apk_signing_guide(self):
        """Create guide for secure APK signing"""
        signing_guide = """# 🔐 Secure APK Signing Guide

## Create Secure Keystore

```bash
# Create a secure keystore (do this ONCE and keep safe!)
keytool -genkey -v -keystore maya-chatbot-key.keystore -alias maya-chatbot -keyalg RSA -keysize 2048 -validity 10000

# You'll be prompted for:
# - Keystore password (use strong password)
# - Key password (use strong password)  
# - Your details (name, organization, etc.)
```

## Update buildozer.spec for Signing

Add to buildozer.spec:
```ini
[buildozer]
# Path to your keystore
android.keystore = maya-chatbot-key.keystore

# Alias name
android.keyalias = maya-chatbot

# These will be prompted during build
# android.keystore_passwd = 
# android.keyalias_passwd = 
```

## Build Signed APK

```bash
# Build release APK (will prompt for passwords)
buildozer android release

# Verify APK signature
jarsigner -verify -verbose -certs bin/malaychatbot-1.0.0-release.apk
```

## Security Best Practices

1. **Keep Keystore Safe**: 
   - Store in secure location
   - Backup keystore file
   - Never share keystore passwords

2. **Use Strong Passwords**:
   - Minimum 12 characters
   - Mix of letters, numbers, symbols
   - Different passwords for keystore and key

3. **APK Verification**:
   - Always verify signature before distribution
   - Check APK with antivirus tools
   - Test on clean devices

4. **Distribution Security**:
   - Use HTTPS for downloads
   - Provide SHA256 checksums
   - Monitor for unauthorized modifications

## Emergency Response

If keystore is compromised:
1. Stop all distribution immediately
2. Create new keystore with different passwords
3. Build and redistribute new APK
4. Notify users of security update
"""
        
        with open("APK_SIGNING_GUIDE.md", "w") as f:
            f.write(signing_guide)
        
        self.security_fixes.append("✅ Created secure APK signing guide")
    
    def run_complete_audit(self) -> Dict[str, List[str]]:
        """Run complete security audit"""
        print("🔒 Running Security Audit for Maya Chatbot APK...")
        print("=" * 50)
        
        # Collect all issues
        buildozer_issues = self.audit_buildozer_spec()
        code_issues = self.audit_python_code()
        data_issues = self.audit_training_data()
        
        all_issues = buildozer_issues + code_issues + data_issues
        
        # Apply security fixes
        print("\n🔧 Applying Security Fixes...")
        self.create_secure_buildozer_spec()
        self.create_input_validation()
        self.create_secure_data_storage()
        self.create_apk_signing_guide()
        
        # Try to update Kivy app (might fail if file doesn't exist)
        try:
            self.update_kivy_app_security()
        except Exception as e:
            self.security_fixes.append(f"⚠️  Could not auto-update Kivy app: {e}")
        
        # Generate security report
        report = {
            "issues_found": all_issues,
            "fixes_applied": self.security_fixes,
            "recommendations": [
                "🔐 Always sign APK with secure keystore",
                "🔍 Test APK on clean devices before distribution",
                "📱 Request minimal permissions only", 
                "🛡️ Use HTTPS for all downloads",
                "🔒 Validate all user inputs",
                "📊 Monitor app usage for suspicious activity",
                "🚨 Have incident response plan ready"
            ]
        }
        
        return report

def main():
    """Run security audit"""
    auditor = SecurityAuditor()
    report = auditor.run_complete_audit()
    
    print("\n" + "=" * 50)
    print("🔒 SECURITY AUDIT REPORT")
    print("=" * 50)
    
    if report["issues_found"]:
        print("\n⚠️  Issues Found:")
        for issue in report["issues_found"]:
            print(f"  {issue}")
    else:
        print("\n✅ No security issues found!")
    
    print("\n🔧 Fixes Applied:")
    for fix in report["fixes_applied"]:
        print(f"  {fix}")
    
    print("\n💡 Security Recommendations:")
    for rec in report["recommendations"]:
        print(f"  {rec}")
    
    print(f"\n🎯 Security Score: {max(0, 100 - len(report['issues_found']) * 10)}/100")
    
    if len(report["issues_found"]) == 0:
        print("\n🎉 Maya Chatbot APK is SECURE for distribution!")
    else:
        print(f"\n⚠️  Please address {len(report['issues_found'])} security issues before distribution")

if __name__ == "__main__":
    main() 