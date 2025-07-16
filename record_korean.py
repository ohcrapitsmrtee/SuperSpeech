# Record and test Korean pronunciation
import os
import wave
import pyaudio
import time
import hashlib
import requests
import json

# API credentials
app_key = "175152606100052e"
secret_key = "8f2d6a0d1d09c1ed9327adb82bd93939"
base_url = "https://api.speechsuper.com/"
user_id = "guest"

# Audio recording settings
CHUNK = 1024
FORMAT = pyaudio.paInt16  # 16-bit format
CHANNELS = 1  # Mono
RATE = 16000  # 16kHz sample rate
RECORD_SECONDS = 3  # Adjust recording length as needed

# Korean word settings
KOREAN_WORD = "???"  # Korean word (convenience store)
ROMANIZED_WORD = "pyeonuijeom"  # Romanized version

# File to save the recording
WAVE_OUTPUT_FILENAME = os.path.join("audio_samples", "korean_word.wav")

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
    
    print(f"Say the Korean word '{KOREAN_WORD}' (pyeonuijeom) after the countdown!")
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

def evaluate_korean(audio_file, use_romanized=False):
    """Evaluate the Korean recording using SpeechSuper API"""
    print("\nEvaluating your Korean pronunciation...")
    
    # Choose which text to use
    ref_text = ROMANIZED_WORD if use_romanized else KOREAN_WORD
    print(f"Using reference text: {ref_text}")
    
    # Generate timestamp and signatures
    timestamp = str(int(time.time()))
    connect_str = (app_key + timestamp + secret_key).encode("utf-8")
    connect_sig = hashlib.sha1(connect_str).hexdigest()
    start_str = (app_key + timestamp + user_id + secret_key).encode("utf-8")
    start_sig = hashlib.sha1(start_str).hexdigest()
    
    # Create API URL
    core_type = "word.eval.promax"
    url = base_url + core_type
    
    # Create request parameters
    params = {
        "connect": {
            "cmd": "connect",
            "param": {
                "sdk": {
                    "version": 16777472,
                    "source": 9,
                    "protocol": 2
                },
                "app": {
                    "applicationId": app_key,
                    "sig": connect_sig,
                    "timestamp": timestamp
                }
            }
        },
        "start": {
            "cmd": "start",
            "param": {
                "app": {
                    "userId": user_id,
                    "applicationId": app_key,
                    "timestamp": timestamp,
                    "sig": start_sig
                },
                "audio": {
                    "audioType": "wav",
                    "channel": 1,
                    "sampleBytes": 2,
                    "sampleRate": RATE
                },
                "request": {
                    "coreType": core_type,
                    "refText": ref_text,
                    "tokenId": "tokenId"
                }
            }
        }
    }
    
    # Send the request
    try:
        data = {'text': json.dumps(params)}
        headers = {"Request-Index": "0"}
        
        with open(audio_file, 'rb') as audio_file_obj:
            files = {"audio": audio_file_obj}
            response = requests.post(url, data=data, headers=headers, files=files)
        
        # Parse the result
        result = json.loads(response.text)
        
        # Print the results
        print(f"\nAPI Response: {result}")
        
        if "errId" in result:
            print(f"Error: {result.get('error', 'Unknown error')}")
        elif "result" in result:
            print(f"\nResults:")
            print(f"Overall Score: {result['result'].get('overall', 'N/A')}")
            print(f"Pronunciation Score: {result['result'].get('pronunciation', 'N/A')}")
        
    except Exception as e:
        print(f"Error: {e}")

def main():
    print("Korean Pronunciation Recording and Testing")
    print("=========================================")
    print(f"You will record yourself saying the Korean word: '{KOREAN_WORD}' (pyeonuijeom)")
    print(f"Recording will last for {RECORD_SECONDS} seconds")
    
    input("Press Enter to start recording...")
    
    # Record audio
    audio_file = record_audio()
    
    # First try with Korean characters
    evaluate_korean(audio_file, use_romanized=False)
    
    # If that fails, try with romanized version
    print("\nNow trying with romanized version...")
    evaluate_korean(audio_file, use_romanized=True)

if __name__ == "__main__":
    main()
