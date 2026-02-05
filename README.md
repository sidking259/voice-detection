🛡️ Voice Defense Pro: Multi-Language AI Voice Detector
Buildathon Project Overview
Voice Defense Pro ek advanced AI-based system hai jo ye determine karta hai ki koi audio sample Insaan (Human) ne record kiya hai ya AI (Synthetic) ne generate kiya hai. Ye project specifically Indian context ke liye banaya gaya hai, jo Tamil, English, Hindi, Malayalam, aur Telugu bhashaon ko support karta hai.

🚀 Key Features
Multi-Language Support: 5 languages ke liye optimized detection.

Real-time API: FastAPI backend jo Base64-encoded MP3 input leta hai aur structured JSON response deta hai.

Expert UI: Streamlit-based dashboard jismein Red/Green signals aur technical explanations milti hain.

High Accuracy: Balanced dataset par trained model jismein 92% validation accuracy achieve ki gayi hai.

🛠️ Tech Stack
Backend: FastAPI (Python)

Frontend: Streamlit

Machine Learning: Scikit-learn (Random Forest Classifier)

Audio Processing: Librosa (MFCC, Spectral Contrast, Chroma features)

Security: Header-based Authentication

🧠 How It Works (The Core Logic)
Hamaara system audio ka "Acoustic MRI" karta hai:

MFCC (Texture): Awaaz ki banaavat aur texture ko analyze karta hai.

Spectral Contrast: AI voices mein milne wali "Mechanical Clarity" aur artifacts ko detect karta hai.

Chroma Features: Pitch aur harmonic patterns ko check karta hai jo multi-language speech mein unique hote hain.

⚙️ Installation & Setup
Environment Setup:

Bash

pip install -r requirements.txt
Run Backend Server:

Bash

uvicorn app:app --reload
Run Frontend UI:

Bash

streamlit run ui.py
📡 API Reference
Detect Voice
Endpoint: POST /detect-voice

Headers: authorization: sid-secret-key-123

Request Body:

JSON

{
  "audio_data": "BASE64_ENCODED_MP3_STRING",
  "language": "Hindi"
}
Response:

JSON

{
  "classification": "........",
  "confidence_score": ......,
  "explanation": "......"
}

💡 Developer
Sid - AI  Developer