import os
import whisper

os.environ["PATH"] += os.pathsep + r"C:\Users\Asus\Downloads\ffmpeg-8.0.1-essentials_build\ffmpeg-8.0.1-essentials_build\bin"

model = whisper.load_model("base")

def transcribe_audio(audio_path):
    result = model.transcribe(audio_path)
    return result["text"]

if __name__ == "__main__":
    audio_file = "sample.wav"  # mp3/wav both ok
    print("\n--- TRANSCRIPT ---")
    print(transcribe_audio(audio_file))

