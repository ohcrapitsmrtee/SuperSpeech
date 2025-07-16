# SuperSpeech Example Application
# This script demonstrates how to use the SuperSpeech API wrapper

import os
import json
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.speech_api import SuperSpeech

# Create a SuperSpeech instance with default API keys
# You can also provide your own keys: SuperSpeech(app_key="your_key", secret_key="your_secret")
api = SuperSpeech()

def evaluate_word():
    """Example of evaluating a single word pronunciation"""
    
    # Audio file path - adjust as needed
    audio_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "audio_samples", "supermarket.wav")
    
    # Reference text for the audio
    ref_text = "supermarket"
    
    # Evaluate the pronunciation
    result = api.evaluate_pronunciation(
        audio_path=audio_path,
        ref_text=ref_text,
        core_type="word.eval.promax"
    )
    
    # Print the result in a readable format
    print("===== Word Pronunciation Evaluation =====")
    print(f"Word: {ref_text}")
    
    if "result" in result:
        overall_score = result["result"]["overall"]
        pronunciation_score = result["result"]["pronunciation"]
        print(f"Overall Score: {overall_score}")
        print(f"Pronunciation Score: {pronunciation_score}")
        
        # Print phoneme details
        print("\nPhoneme Details:")
        if "words" in result["result"] and result["result"]["words"]:
            word = result["result"]["words"][0]
            if "phonics" in word:
                for phoneme_data in word["phonics"][0]:
                    print(f"  Phoneme: {phoneme_data['phoneme']}, " 
                          f"Spell: {phoneme_data['spell']}, "
                          f"Score: {phoneme_data['overall']}")
    else:
        print("Error in evaluation:", result.get("error", "Unknown error"))

def evaluate_sentence():
    """Example of evaluating a sentence pronunciation"""
    
    # This is just an example - you would need a proper sentence audio file
    print("\n===== Sentence Evaluation =====")
    print("This feature requires a sentence audio file.")
    print("To test sentence evaluation:")
    print("1. Prepare a sentence audio file (e.g., 'my_sentence.wav')")
    print("2. Use the following code:")
    print("""
    api.evaluate_pronunciation(
        audio_path="path/to/my_sentence.wav",
        ref_text="This is the reference sentence.",
        core_type="sent.eval.promax"
    )
    """)

def evaluate_spontaneous():
    """Example of evaluating spontaneous speech"""
    
    # This is just an example - you would need a proper speech audio file
    print("\n===== Spontaneous Speech Evaluation =====")
    print("This feature requires a spontaneous speech audio file.")
    print("To test spontaneous speech evaluation:")
    print("1. Prepare a speech audio file (e.g., 'my_speech.wav')")
    print("2. Use the following code:")
    print("""
    api.evaluate_spontaneous_speech(
        audio_path="path/to/my_speech.wav",
        question_prompt="What's your favorite food?",
        test_type="ielts",
        model="non_native"
    )
    """)

if __name__ == "__main__":
    print("SuperSpeech API Example Application")
    print("-----------------------------------")
    
    # Example of word pronunciation evaluation
    evaluate_word()
    
    # Example of sentence pronunciation evaluation
    evaluate_sentence()
    
    # Example of spontaneous speech evaluation
    evaluate_spontaneous()
