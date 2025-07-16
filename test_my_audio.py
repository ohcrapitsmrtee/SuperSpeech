# Test script for using your own audio file
import os
from src.speech_api import SuperSpeech

# Initialize the API
api = SuperSpeech()

# Replace this with the name of your audio file
YOUR_AUDIO_FILE = "your_recording.wav"  # You'll need to place this in the audio_samples folder

# Replace this with the text that is spoken in your audio file
YOUR_REFERENCE_TEXT = "supermarket"  # Change this to match what you're saying

# Path to your audio file
audio_path = os.path.join("audio_samples", YOUR_AUDIO_FILE)

print("SuperSpeech Test with Custom Audio")
print("----------------------------------")
print(f"Testing audio file: {YOUR_AUDIO_FILE}")
print(f"Reference text: {YOUR_REFERENCE_TEXT}")

# Check if the file exists
if not os.path.exists(audio_path):
    print(f"ERROR: Audio file not found at {audio_path}")
    print("Please place your audio file in the audio_samples directory")
    exit(1)

# Evaluate the pronunciation
result = api.evaluate_pronunciation(
    audio_path=audio_path,
    ref_text=YOUR_REFERENCE_TEXT,
    core_type="word.eval.promax"  # Use "sent.eval.promax" for sentences
)

# Print the results
if "result" in result:
    print("\nResults:")
    print(f"Overall Score: {result['result'].get('overall', 'N/A')}")
    print(f"Pronunciation Score: {result['result'].get('pronunciation', 'N/A')}")
    
    # More detailed results if available
    if "words" in result["result"] and result["result"]["words"]:
        word = result["result"]["words"][0]
        if "phonics" in word and word["phonics"]:
            print("\nPhoneme Details:")
            for phoneme_data in word["phonics"][0]:
                print(f"  Phoneme: {phoneme_data.get('phoneme', 'N/A')}, " 
                      f"Spell: {phoneme_data.get('spell', 'N/A')}, "
                      f"Score: {phoneme_data.get('overall', 'N/A')}")
else:
    print("Error in evaluation:", result.get("error", "Unknown error"))
    if "applicationId" in result:
        print("API returned:", result)
