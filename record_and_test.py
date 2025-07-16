# Record and test your voice with SuperSpeech API
import os
import wave
import pyaudio
import time
from src.speech_api import SuperSpeech

# Audio recording settings
CHUNK = 1024
FORMAT = pyaudio.paInt16  # 16-bit format
CHANNELS = 1  # Mono
RATE = 16000  # 16kHz sample rate
RECORD_SECONDS = 3  # Adjust recording length as needed

# File to save the recording
WAVE_OUTPUT_FILENAME = os.path.join("audio_samples", "my_recording.wav")

# The word or phrase you'll say
REFERENCE_TEXT = "supermarket"  # Change this to what you plan to say!

def record_audio():
    """Record audio from microphone"""
    print("Recording Setup...")
    p = pyaudio.PyAudio()
    
    # Open stream
    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)
    
    print(f"Say '{REFERENCE_TEXT}' after the countdown!")
    for i in range(3, 0, -1):
        print(f"{i}...")
        time.sleep(1)
    
    print("Recording NOW!")
    
    frames = []
    
    # Record audio in chunks
    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)
    
    print("Recording complete!")
    
    # Stop and close the stream
    stream.stop_stream()
    stream.close()
    p.terminate()
    
    # Save the recorded data as a WAV file
    os.makedirs(os.path.dirname(WAVE_OUTPUT_FILENAME), exist_ok=True)
    wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()
    
    print(f"Audio saved to {WAVE_OUTPUT_FILENAME}")
    return WAVE_OUTPUT_FILENAME

def evaluate_recording(audio_file, ref_text):
    """Evaluate the recording using SuperSpeech API"""
    print("\nEvaluating your pronunciation...")
    api = SuperSpeech()
    
    # Evaluate the pronunciation
    result = api.evaluate_pronunciation(
        audio_path=audio_file,
        ref_text=ref_text,
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

def main():
    print("SuperSpeech Voice Recording and Testing")
    print("======================================")
    print(f"You will record yourself saying: '{REFERENCE_TEXT}'")
    print(f"Recording will last for {RECORD_SECONDS} seconds")
    
    input("Press Enter to start recording...")
    
    # Record audio
    audio_file = record_audio()
    
    # Evaluate the recording
    evaluate_recording(audio_file, REFERENCE_TEXT)

if __name__ == "__main__":
    main()
