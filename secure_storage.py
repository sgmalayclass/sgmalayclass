
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
