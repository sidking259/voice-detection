import base64

with open("test.mp3", "rb") as audio:
    encoded = base64.b64encode(audio.read()).decode()

print(encoded)
