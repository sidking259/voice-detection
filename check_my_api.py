import requests
import base64
import os

# --- CONFIGURATION ---
API_URL = "http://127.0.0.1:8000/detect-voice"  # Tera Local Server
AUDIO_FILE = "test.mp3"  # Jo audio file hum bhejenge
AUTH_KEY = "sid-secret-key-123"

def test_api():
    # 1. Check karna ki file hai ya nahi
    if not os.path.exists(AUDIO_FILE):
        print(f"❌ Bhai '{AUDIO_FILE}' nahi mili! Folder mein koi MP3 file daal de.")
        return

    print(f"🎧 '{AUDIO_FILE}' ko padh raha hoon...")
    
    # 2. Audio ko Base64 Text mein convert karna
    with open(AUDIO_FILE, "rb") as audio_file:
        encoded_string = base64.b64encode(audio_file.read()).decode('utf-8')

    # 3. Data packet taiyar karna
    payload = {
        "audio_data": encoded_string,
        "language": "Hindi"
    }
    
    headers = {
        "authorization": AUTH_KEY
    }

    # 4. Server ko bhejna
    print("🚀 Server ko data bhej raha hoon... Wait kar...")
    try:
        response = requests.post(API_URL, json=payload, headers=headers)
        
        # 5. Result dikhana
        if response.status_code == 200:
            print("\n✅ SUCCESS! Server ne jawab diya:")
            print(response.json())
        else:
            print(f"\n❌ Error aaya bhai: {response.status_code}")
            print(response.text)
            
    except Exception as e:
        print(f"\n❌ Connection Fail: {e}")
        print("Kya tera 'uvicorn' wala terminal chal raha hai?")

if __name__ == "__main__":
    test_api()