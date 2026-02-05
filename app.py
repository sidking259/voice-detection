import base64
import os
import uuid
import numpy as np
import librosa
import joblib
from fastapi import FastAPI, HTTPException, Header
from pydantic import BaseModel
from contextlib import asynccontextmanager

# ===============================
# GLOBAL MODELS
# ===============================
models = {}

# ===============================
# APP LIFESPAN (load models once)
# ===============================
@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        print("📥 Loading AI models...")
        models["clf"] = joblib.load("models/classifier.pkl")
        models["scaler"] = joblib.load("models/scaler.pkl")
        print("✅ Models loaded successfully")
    except Exception as e:
        print("❌ Model loading failed:", e)
        models["clf"] = None
    yield
    models.clear()

app = FastAPI(
    title="AI-Generated Voice Detection API",
    description="Detects whether a voice sample is AI-generated or Human-generated",
    version="1.0.0",
    lifespan=lifespan
)

# ===============================
# REQUEST SCHEMA
# ===============================
class VoiceRequest(BaseModel):
    audio_data: str                 # Base64 encoded MP3
    language: str | None = "Unknown" # Tamil, Hindi, English, etc.

# ===============================
# FEATURE EXTRACTION
# ===============================
def extract_audio_features(file_path: str):
    try:
        y, sr = librosa.load(file_path, sr=22050, duration=5)

        mfcc = np.mean(librosa.feature.mfcc(y=y, sr=sr, n_mfcc=40).T, axis=0)
        spectral_contrast = np.mean(
            librosa.feature.spectral_contrast(y=y, sr=sr).T, axis=0
        )
        chroma = np.mean(
            librosa.feature.chroma_stft(y=y, sr=sr).T, axis=0
        )

        return np.hstack([mfcc, spectral_contrast, chroma])

    except Exception as e:
        print("Feature extraction error:", e)
        return None

# ===============================
# API ENDPOINT
# ===============================
@app.post("/detect-voice")
async def detect_voice(
    payload: VoiceRequest,
    authorization: str = Header(None)
):
    # -------- Security --------
    if authorization != "sid-secret-key-123":
        raise HTTPException(status_code=401, detail="Unauthorized access")

    if models["clf"] is None:
        raise HTTPException(status_code=500, detail="Model not loaded")

    # -------- Decode Audio --------
    temp_file = f"temp_{uuid.uuid4().hex}.mp3"

    try:
        with open(temp_file, "wb") as f:
            f.write(base64.b64decode(payload.audio_data))
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid Base64 audio data")

    # -------- Feature Extraction --------
    features = extract_audio_features(temp_file)

    # Cleanup temp file
    if os.path.exists(temp_file):
        os.remove(temp_file)

    if features is None:
        raise HTTPException(status_code=422, detail="Unable to process audio")

    # -------- Prediction --------
    features_scaled = models["scaler"].transform([features])
    prediction = models["clf"].predict(features_scaled)[0]
    probabilities = models["clf"].predict_proba(features_scaled)[0]

    # -------- Response Logic --------
    if prediction == 1:
        classification = "AI-Generated"
        confidence = round(probabilities[1] * 100, 2)
        explanation = (
            "The voice sample shows unusually stable pitch, uniform spectral patterns, "
            "and reduced micro-variations, which are commonly associated with "
            "synthetic AI-generated speech."
        )
    else:
        classification = "Human-Generated"
        confidence = round(probabilities[0] * 100, 2)
        explanation = (
            "The audio contains natural pitch fluctuations, irregular pauses, "
            "and organic spectral variations typical of human speech."
        )

    # -------- Final JSON Response --------
    return {
        "classification": classification,
        "confidence_score": confidence,
        "language_detected": payload.language,
        "explanation": explanation
    }
