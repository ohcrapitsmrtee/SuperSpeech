# Test Korean pronunciation with different approaches
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

# Audio settings
audio_path = os.path.join("audio_samples", "korean_word.wav")  # You'll need to record this
audio_type = "wav"
audio_sample_rate = 16000

# Different approaches to test
tests = [
    {
        "name": "Korean UTF-8",
        "core_type": "word.eval.promax",
        "ref_text": "???"  # Original Korean
    },
    {
        "name": "Korean Romanized",
        "core_type": "word.eval.promax",
        "ref_text": "pyeonuijeom"  # Romanized version
    },
    {
        "name": "Korean with different core type",
        "core_type": "word.eval",  # Try different core type
        "ref_text": "???"
    },
    {
        "name": "Korean with language code",
        "core_type": "word.eval.promax",
        "ref_text": "???",
        "language": "ko-KR"  # Try adding language code
    }
]

def test_korean_pronunciation(test_config):
    """Test Korean pronunciation with given configuration"""
    print(f"\n--- Testing: {test_config['name']} ---")
    print(f"Core Type: {test_config['core_type']}")
    print(f"Reference Text: {test_config['ref_text']}")
    
    # Generate timestamp and signatures
    timestamp = str(int(time.time()))
    connect_str = (app_key + timestamp + secret_key).encode("utf-8")
    connect_sig = hashlib.sha1(connect_str).hexdigest()
    start_str = (app_key + timestamp + user_id + secret_key).encode("utf-8")
    start_sig = hashlib.sha1(start_str).hexdigest()
    
    # Create API URL
    url = base_url + test_config['core_type']
    
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
                    "coreType": test_config['core_type'],
                    "refText": test_config['ref_text'],
                    "tokenId": "tokenId"
                }
            }
        }
    }
    
    # Add language if specified
    if "language" in test_config:
        params["start"]["param"]["request"]["language"] = test_config["language"]
    
    try:
        # Convert parameters to JSON
        data = {'text': json.dumps(params)}
        headers = {"Request-Index": "0"}
        
        # Check if audio file exists
        if not os.path.exists(audio_path):
            print(f"WARNING: Audio file {audio_path} not found.")
            print("This is a dry run to check API acceptance, not actual evaluation.")
            return
            
        # Send request with audio file
        with open(audio_path, 'rb') as audio_file:
            files = {"audio": audio_file}
            response = requests.post(url, data=data, headers=headers, files=files)
            
        # Parse and print response
        result = json.loads(response.text)
        print(f"API Response: {result}")
        
        if "errId" in result:
            print(f"Error: {result.get('error', 'Unknown error')}")
        elif "result" in result:
            print(f"Success! Overall Score: {result['result'].get('overall', 'N/A')}")
            print(f"Pronunciation Score: {result['result'].get('pronunciation', 'N/A')}")
            
    except Exception as e:
        print(f"Exception: {e}")

def main():
    print("Korean Pronunciation Test")
    print("=========================")
    
    # First, let's create a simple recorder to get a Korean audio sample
    if not os.path.exists(audio_path):
        print(f"NOTE: No audio file found at {audio_path}")
        print("You'll need to record the Korean word '???' to test properly.")
        print("This script will still run API tests without audio to check if the API accepts Korean.")
        print("It will create an empty audio file for testing purposes.")
        
        # Create an empty directory if needed
        os.makedirs(os.path.dirname(audio_path), exist_ok=True)
        
        # Create an empty file for testing if it doesn't exist
        with open(audio_path, 'wb') as f:
            pass
    
    # Run each test configuration
    for test_config in tests:
        test_korean_pronunciation(test_config)

if __name__ == "__main__":
    main()
