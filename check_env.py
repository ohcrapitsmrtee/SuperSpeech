import sys
import os

# Print Python version and environment
print(f"Python version: {sys.version}")
print(f"Current directory: {os.getcwd()}")

# Check if audio file exists
audio_path = os.path.join("audio_samples", "supermarket.wav")
print(f"Audio file exists: {os.path.exists(audio_path)}")
