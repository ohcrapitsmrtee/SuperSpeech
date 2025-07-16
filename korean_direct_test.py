# Direct test for Korean word pronunciation
import os
import time
import hashlib
import requests
import json

# API credentials
app_key = "175152606100052e"
secret_key = "8f2d6a0d1d09c1ed9327adb82bd93939"
base_url = "https://api.speechsuper.com/"
user_id = "guest"

# Audio file settings
audio_path = os.path.join("audio_samples", "korean_word.wav")  # This will be created when you record
ref_text = "???"  # Korean for "convenience store"
core_type = "word.eval.promax"
audio_type = "wav"
audio_sample_rate = 16000

# Recording settings
import wave
import pyaudio

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
RECORD_SECONDS = 3

def record_audio():
    """Record audio from microphone"""
    print("Recording Setup...")
    p = pyaudio.PyAudio()
    
    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)
    
    print(f"Say '{ref_text}' (convenience store in Korean) after the countdown!")
    for i in range(3, 0, -1):
        print(f"{i}...")
        time.sleep(1)
    
    print("Recording NOW!")
    
    frames = []
    
    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)
    
    print("Recording complete!")
    
    stream.stop_stream()
    stream.close()
    p.terminate()
    
    os.makedirs(os.path.dirname(audio_path), exist_ok=True)
    wf = wave.open(audio_path, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()
    
    print(f"Audio saved to {audio_path}")

def evaluate_pronunciation():
    """Send the recorded audio to the API for evaluation"""
    print("\nEvaluating your Korean pronunciation...")
    
    # Generate timestamp and signatures
    timestamp = str(int(time.time()))
    connect_str = (app_key + timestamp + secret_key).encode("utf-8")
    connect_sig = hashlib.sha1(connect_str).hexdigest()
    start_str = (app_key + timestamp + user_id + secret_key).encode("utf-8")
    start_sig = hashlib.sha1(start_str).hexdigest()
    
    # Create API URL
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
                    "audioType": audio_type,
                    "channel": 1,
                    "sampleBytes": 2,
                    "sampleRate": audio_sample_rate
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
        
        with open(audio_path, 'rb') as audio_file:
            files = {"audio": audio_file}
            response = requests.post(url, data=data, headers=headers, files=files)
            
        result = json.loads(response.text)
        
        # Print the results
        if "result" in result:
            print("\nResults:")
            print(f"Overall Score: {result['result'].get('overall', 'N/A')}")
            print(f"Pronunciation Score: {result['result'].get('pronunciation', 'N/A')}")
            
            # Print full response for debugging
            print("\nFull API Response:")
            print(json.dumps(result, indent=2, ensure_ascii=False))
        else:
            print("Error in evaluation:", result.get("error", "Unknown error"))
            print("API returned:", result)
                
    except Exception as e:
        print(f"Error: {e}")

def main():
    print("SuperSpeech Korean Pronunciation Test")
    print("===================================")
    
    # Ask to start recording
    input("Press Enter to start recording...")
    
    # Record audio
    record_audio()
    
    # Check if file exists before evaluating
    if os.path.exists(audio_path):
        evaluate_pronunciation()
    else:
        print(f"Error: Audio file {audio_path} was not created properly.")

if __name__ == "__main__":
    main()
