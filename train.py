import os
import numpy as np
import librosa
import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

# ===============================
# CONFIGURATION
# ===============================
DATASET_PATH = "dataset"
MODEL_DIR = "models"
SAMPLE_RATE = 22050
DURATION = 5  # seconds
RANDOM_STATE = 42

os.makedirs(MODEL_DIR, exist_ok=True)

# ===============================
# FEATURE EXTRACTION
# ===============================
def extract_features(file_path: str):
    """
    Extracts robust audio features used for AI vs Human voice detection.
    """
    try:
        y, sr = librosa.load(
            file_path,
            sr=SAMPLE_RATE,
            duration=DURATION
        )

        mfcc = np.mean(
            librosa.feature.mfcc(y=y, sr=sr, n_mfcc=40).T,
            axis=0
        )

        spectral_contrast = np.mean(
            librosa.feature.spectral_contrast(y=y, sr=sr).T,
            axis=0
        )

        chroma = np.mean(
            librosa.feature.chroma_stft(y=y, sr=sr).T,
            axis=0
        )

        return np.hstack([mfcc, spectral_contrast, chroma])

    except Exception as e:
        print(f"⚠️ Skipped file: {file_path} | Reason: {e}")
        return None

# ===============================
# DATA LOADING
# ===============================
def load_dataset():
    features = []
    labels = []

    for label_name, label_value in [("real", 0), ("fake", 1)]:
        folder_path = os.path.join(DATASET_PATH, label_name)

        if not os.path.exists(folder_path):
            print(f"❌ Missing folder: {folder_path}")
            continue

        print(f"📂 Loading {label_name.upper()} voices...")

        for file in os.listdir(folder_path):
            file_path = os.path.join(folder_path, file)

            feat = extract_features(file_path)
            if feat is not None:
                features.append(feat)
                labels.append(label_value)

    return np.array(features), np.array(labels)

# ===============================
# TRAINING PIPELINE
# ===============================
def train_model():
    print("🚀 Starting AI Voice Detection Training Pipeline")

    X, y = load_dataset()

    # ---------------- Validation ----------------
    if len(X) < 20:
        print("❌ ERROR: Dataset too small!")
        print("👉 Minimum recommended: 10 Human + 10 AI samples")
        return

    print(f"✅ Total samples loaded: {len(X)}")

    # ---------------- Scaling ----------------
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # ---------------- Train / Test Split ----------------
    X_train, X_test, y_train, y_test = train_test_split(
        X_scaled,
        y,
        test_size=0.2,
        random_state=RANDOM_STATE,
        stratify=y
    )

    # ---------------- Model ----------------
    clf = RandomForestClassifier(
        n_estimators=200,
        random_state=RANDOM_STATE,
        n_jobs=-1
    )

    clf.fit(X_train, y_train)

    # ---------------- Evaluation ----------------
    y_pred = clf.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred) * 100

    print(f"🎯 Validation Accuracy: {accuracy:.2f}%")

    # ---------------- Save Artifacts ----------------
    joblib.dump(clf, os.path.join(MODEL_DIR, "classifier.pkl"))
    joblib.dump(scaler, os.path.join(MODEL_DIR, "scaler.pkl"))

    print("💾 Model & Scaler saved successfully in 'models/'")
    print("✅ Training pipeline completed")

# ===============================
# ENTRY POINT
# ===============================
if __name__ == "__main__":
    train_model()
