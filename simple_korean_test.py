# Simple Korean test using romanization
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

# Audio file path (use the default supermarket.wav for testing)
audio_path = os.path.join("audio_samples", "supermarket.wav")

# Instead of using Korean characters, use the romanized version
romanized_text = "pyeonuijeom"  # This is the romanization of ??? (convenience store)

print("SuperSpeech Korean Test (Romanized)")
print("===================================")
print(f"Testing with audio file: {audio_path}")
print(f"Reference text (romanized): {romanized_text}")

# Check if the file exists
if not os.path.exists(audio_path):
    print(f"ERROR: Audio file not found at {audio_path}")
    exit(1)

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
                "sampleRate": 16000
            },
            "request": {
                "coreType": core_type,
                "refText": romanized_text,
                "tokenId": "tokenId"
            }
        }
    }
}

print("Sending request to SpeechSuper API...")

# Send the request
try:
    data = {'text': json.dumps(params)}
    headers = {"Request-Index": "0"}
    
    with open(audio_path, 'rb') as audio_file:
        files = {"audio": audio_file}
        response = requests.post(url, data=data, headers=headers, files=files)
    
    # Parse and print response
    result = json.loads(response.text)
    print(f"API Response: {result}")
    
    if "errId" in result:
        print(f"Error: {result.get('error', 'Unknown error')}")
    elif "result" in result:
        print(f"\nResults:")
        print(f"Overall Score: {result['result'].get('overall', 'N/A')}")
        print(f"Pronunciation Score: {result['result'].get('pronunciation', 'N/A')}")
        
except Exception as e:
    print(f"Exception: {e}")

print("\nNOTE: To test with your own voice saying the Korean word:")
print("1. Run 'python record_korean.py' to record and test")
print("2. It will try both Korean characters and romanization")
