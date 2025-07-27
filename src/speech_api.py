# SuperSpeech API Wrapper
# Based on SpeechSuper API Samples
# https://github.com/speechsuper/speechsuper-api-samples

import time
import hashlib
import requests
import json
import os

class SuperSpeech:
    def __init__(self, app_key="175152606100052e", secret_key="8f2d6a0d1d09c1ed9327adb82bd93939"):
        """Initialize SuperSpeech with your API credentials.
        
        Args:
            app_key (str): Your SpeechSuper application key
            secret_key (str): Your SpeechSuper secret key
        """
        self.app_key = app_key
        self.secret_key = secret_key
        self.base_url = "https://api.speechsuper.com/"
        self.user_id = "guest"
    
    def _generate_timestamp(self):
        """Generate current timestamp for API requests (in milliseconds to match WebSocket)."""
        return str(int(time.time() * 1000))
    
    def _generate_signatures(self, timestamp):
        """Generate required signatures for API authentication.
        
        Args:
            timestamp (str): Current timestamp
            
        Returns:
            tuple: (connect_sig, start_sig) signature pair
        """
        connect_str = (self.app_key + timestamp + self.secret_key).encode("utf-8")
        connect_sig = hashlib.sha1(connect_str).hexdigest()
        
        start_str = (self.app_key + timestamp + self.user_id + self.secret_key).encode("utf-8")
        start_sig = hashlib.sha1(start_str).hexdigest()
        
        return connect_sig, start_sig
    
    def evaluate_pronunciation(self, audio_path, ref_text, core_type="word.eval.promax", 
                              audio_type="wav", audio_sample_rate=16000):
        """Evaluate pronunciation using SpeechSuper API.
        
        Args:
            audio_path (str): Path to the audio file
            ref_text (str): Reference text for evaluation
            core_type (str): API evaluation type (default: word.eval.promax)
            audio_type (str): Audio file format (default: wav)
            audio_sample_rate (int): Audio sample rate (default: 16000)
            
        Returns:
            dict: Evaluation results from the API
        """
        timestamp = self._generate_timestamp()
        connect_sig, start_sig = self._generate_signatures(timestamp)
        
        url = self.base_url + core_type
        
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
                        "applicationId": self.app_key,
                        "sig": connect_sig,
                        "timestamp": timestamp
                    }
                }
            },
            "start": {
                "cmd": "start",
                "param": {
                    "app": {
                        "userId": self.user_id,
                        "applicationId": self.app_key,
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
        
        data = {'text': json.dumps(params)}
        headers = {"Request-Index": "0"}
        
        try:
            with open(audio_path, 'rb') as audio_file:
                files = {"audio": audio_file}
                response = requests.post(url, data=data, headers=headers, files=files)
                
                print(f"Response status code: {response.status_code}")
                print(f"Response text: {response.text}")
                
                if response.text.strip():
                    return json.loads(response.text)
                else:
                    return {"error": f"Empty response from API. Status code: {response.status_code}"}
        except json.JSONDecodeError as e:
            return {"error": f"JSON decode error: {str(e)}. Raw response: {response.text}"}
        except Exception as e:
            return {"error": str(e)}
    
    def evaluate_spontaneous_speech(self, audio_path, question_prompt, 
                                   test_type="ielts", model="non_native", 
                                   penalize_offtopic=1, audio_type="wav", 
                                   audio_sample_rate=16000):
        """Evaluate spontaneous speech using SpeechSuper API.
        
        Args:
            audio_path (str): Path to the audio file
            question_prompt (str): Question prompt for scoring relevance
            test_type (str): Test type (default: ielts)
            model (str): Transcription model (default: non_native)
            penalize_offtopic (int): Whether to penalize off-topic responses (default: 1)
            audio_type (str): Audio file format (default: wav)
            audio_sample_rate (int): Audio sample rate (default: 16000)
            
        Returns:
            dict: Evaluation results from the API
        """
        timestamp = self._generate_timestamp()
        connect_sig, start_sig = self._generate_signatures(timestamp)
        
        url = self.base_url + "speak.eval.pro"
        
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
                        "applicationId": self.app_key,
                        "sig": connect_sig,
                        "timestamp": timestamp
                    }
                }
            },
            "start": {
                "cmd": "start",
                "param": {
                    "app": {
                        "userId": self.user_id,
                        "applicationId": self.app_key,
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
                        "coreType": "speak.eval.pro",
                        "testType": test_type,
                        "questionPrompt": question_prompt,
                        "model": model,
                        "penalizeOfftopic": penalize_offtopic,
                        "tokenId": "tokenId"
                    }
                }
            }
        }
        
        data = {'text': json.dumps(params)}
        headers = {"Request-Index": "0"}
        
        try:
            with open(audio_path, 'rb') as audio_file:
                files = {"audio": audio_file}
                response = requests.post(url, data=data, headers=headers, files=files)
                return json.loads(response.text)
        except Exception as e:
            return {"error": str(e)}
