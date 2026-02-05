import streamlit as st
import requests
import base64
import uuid

# --- PAGE CONFIG ---
st.set_page_config(page_title="Voice Defense Pro", page_icon="🛡️", layout="wide")

# --- CUSTOM CSS (Pro Look & Signals) ---
st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .stButton>button { width: 100%; border-radius: 5px; height: 3.5em; background-color: #FF4B4B; color: white; font-weight: bold; font-size: 18px;}
    .result-card { padding: 20px; border-radius: 10px; background-color: white; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
    /* Signal Box Styles */
    .signal-box { padding: 20px; border-radius: 10px; text-align: center; margin-bottom: 20px; border: 3px solid; }
    .ai-signal { background-color: #ffebee; border-color: #ffcdd2; color: #c62828; }
    .human-signal { background-color: #e8f5e9; border-color: #c8e6c9; color: #2e7d32; }
    .signal-text { font-size: 32px; font-weight: 800; margin: 0; letter-spacing: 2px; }
    </style>
    """, unsafe_allow_html=True)

# --- HEADER ---
st.title("🛡️ Voice Defense Pro")
st.markdown("##### Enterprise-Grade AI Voice Detection (Multi-Language Support)")
st.divider()

# --- SIDEBAR ---
with st.sidebar:
    st.header("⚙️ System Config")
    api_url = st.text_input("API Endpoint", value="http://127.0.0.1:8000/detect-voice")
    auth_key = st.text_input("Auth Key", value="sid-secret-key-123", type="password")
    st.success("API Status: Connected ✅")

# --- MAIN UI ---
col1, col2 = st.columns([1, 1], gap="large")

# === Left Column: Upload ===
with col1:
    st.subheader("📁 Upload Sample")
    uploaded_file = st.file_uploader("Upload Audio (MP3/WAV)", type=["mp3", "wav"])
    
    if uploaded_file is not None:
        st.audio(uploaded_file, format='audio/mp3')
        
        if st.button("🔍 START DETECTION"):
            # Prepare Data
            audio_bytes = uploaded_file.read()
            base64_audio = base64.b64encode(audio_bytes).decode('utf-8')
            
            # Manual language selection hat gaya, ab API handle karega
            payload = {
                "audio_data": base64_audio,
                "language": "Auto-Detect" 
            }
            headers = {"authorization": auth_key}

            with st.spinner("Analyzing spectral artifacts..."):
                try:
                    response = requests.post(api_url, json=payload, headers=headers)
                    if response.status_code == 200:
                        st.session_state['result'] = response.json()
                    else:
                        st.error(f"Error: {response.status_code}")
                except Exception as e:
                    st.error(f"Connection Error: {e}")

# === Right Column: Result Signals ===
with col2:
    st.subheader("⚡ Detection Result")
    
    if 'result' in st.session_state:
        res = st.session_state['result']
        
        # Determine Signal Type
        is_ai = "AI" in res['classification']
        sig_class = "ai-signal" if is_ai else "human-signal"
        sig_text = "AI VOICE" if is_ai else "HUMAN VOICE"
        sig_icon = "🚨" if is_ai else "✅"
        bar_color = "#ff4b4b" if is_ai else "#4CAF50"

        # 1. BIG SIGNAL BOX
        st.markdown(f"""
        <div class="signal-box {sig_class}">
            <p class="signal-text">{sig_icon} {sig_text}</p>
        </div>
        """, unsafe_allow_html=True)

        # 2. DETAILS
        with st.container(border=True):
            # Language Display (Ab yahan dikhega)
            lang = res.get('language_detected', 'Auto-Detected')
            st.markdown(f"**Detected Language:** `{lang}`")
            
            # Confidence Score
            score = res.get('confidence_score', 0.0)
            display_score = score if score > 1 else score * 100
            st.write(f"**Confidence:** {display_score:.2f}%")
            st.progress(int(display_score) / 100)
            
            # Explanation
            st.markdown(f"**Technical Analysis:** {res.get('explanation', 'Analysis complete.')}")
    else:
        st.info("Upload a file and click 'Start Detection' to see results.")

st.divider()
st.caption("Sid's Buildathon Project | AI-Generated Voice Detection System")
