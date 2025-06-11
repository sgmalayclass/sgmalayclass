
def sanitize_user_input(user_input: str) -> str:
    """
    Sanitize user input to prevent security issues
    """
    if not isinstance(user_input, str):
        return ""
    
    # Remove potentially dangerous characters
    dangerous_chars = ['<', '>', '"', "'", '&', '\n', '\r', '\t']
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
