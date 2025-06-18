import json

def load_json():
    try:
        with open("config.json", "r", encoding="utf-8") as f:
            data = json.load(f)
            if isinstance(data, dict):
                return data
            return {"language": "ru", "theme": "l"}
    except (FileNotFoundError, json.JSONDecodeError):
        return {"language": "ru", "theme": "l"}

def load_language():
    config = load_json()
    return config.get("language", "ru")  
    
def load_theme():
    config = load_json()
    return config.get("theme", "l")