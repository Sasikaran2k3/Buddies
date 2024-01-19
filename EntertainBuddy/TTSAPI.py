import requests
import soundfile as sf

API_URL = "https://api-inference.huggingface.co/models/facebook/mms-tts-eng"
headers = {"Authorization": "Bearer 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"}

text = "Our ideal Sunday at home with Vamika?"
response = requests.post(API_URL, headers=headers, json={"inputs": text})
audio_bytes = response.content

# Save the audio to a file
file_path = "output_audio.flac"  # Choose your desired file format (e.g., flac, wav)
sf.write(file_path, audio_bytes, samplerate=22050)  # Adjust the sample_rate if needed

# Get the duration of the audio in seconds
duration = len(audio_bytes) / (2 * 22050)  # 2 bytes per sample

# Display the audio and duration
from IPython.display import Audio, display
display(Audio(data=audio_bytes, rate=22050, autoplay=False))
print(f"Audio duration: {duration} seconds")

# Provide a link to the saved file
from IPython.display import FileLink
FileLink(file_path)
