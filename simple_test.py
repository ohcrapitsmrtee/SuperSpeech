# Simple test using the included supermarket.wav file
import os
from src.speech_api import SuperSpeech

print("SuperSpeech Simple Test")
print("======================")

# Initialize the API
api = SuperSpeech()

# Use the sample audio file that's already included
audio_path = os.path.join("audio_samples", "supermarket.wav")
ref_text = "supermarket"

print(f"Testing with audio file: {audio_path}")
print(f"Reference text: {ref_text}")

# Check if the file exists
if not os.path.exists(audio_path):
    print(f"ERROR: Audio file not found at {audio_path}")
    exit(1)

print("Evaluating pronunciation...")
# Evaluate the pronunciation
result = api.evaluate_pronunciation(
    audio_path=audio_path,
    ref_text=ref_text,
    core_type="word.eval.promax"
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
