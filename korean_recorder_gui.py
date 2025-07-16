import tkinter as tk
from tkinter import ttk
import pyaudio
import wave
import os
import json
import re
from src.speech_api import SuperSpeech

# Simple Korean to romanization mapping for common words
korean_to_roman = {
    "편의점": "pyeonuijeom",
    "안녕하세요": "annyeonghaseyo", 
    "감사합니다": "gamsahamnida",
    "사랑": "sarang",
    "학교": "hakgyo",
    "친구": "chingu",
    "가족": "gajok",
    "음식": "eumsik",
    "물": "mul",
    "책": "chaek",
    "집": "jip",
    "병원": "byeongwon",
    "음료수": "eumnyosu",
    "커피": "keopi",
    "빵": "ppang",
    "고맙습니다": "gomapseumnida",
    "네": "ne",
    "아니요": "aniyo",
    "좋아요": "johayo",
    "맛있어요": "masisseoyo"
}

class KoreanRecorderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Korean Pronunciation Tester")
        
        # Configure main window
        self.root.geometry("400x300")
        self.root.configure(padx=20, pady=20)
        
        # Initialize audio settings
        self.chunk = 1024
        self.format = pyaudio.paInt16
        self.channels = 1
        self.rate = 16000
        self.frames = []
        self.recording = False
        self.p = pyaudio.PyAudio()
        
        # Create widgets
        self.setup_ui()
        
        # Initialize SuperSpeech API
        self.api = SuperSpeech()
        
    def setup_ui(self):
        # Korean word entry
        ttk.Label(self.root, text="Enter Korean Word:").pack(pady=5)
        self.word_entry = ttk.Entry(self.root)
        self.word_entry.pack(pady=5)
        
        # Example label
        ttk.Label(self.root, text="Korean words auto-convert to romanized (편의점 → pyeonuijeom)", font=('Arial', 8)).pack(pady=2)
        
        # Record button
        self.record_button = ttk.Button(
            self.root, 
            text="Start Recording",
            command=self.toggle_recording
        )
        self.record_button.pack(pady=20)
        
        # Status label
        self.status_label = ttk.Label(self.root, text="")
        self.status_label.pack(pady=10)
        
        # Result label
        self.result_label = ttk.Label(self.root, text="", wraplength=350)
        self.result_label.pack(pady=10)
    
    def toggle_recording(self):
        if not self.recording:
            self.start_recording()
        else:
            self.stop_recording()
    
    def start_recording(self):
        self.recording = True
        self.frames = []
        self.record_button.config(text="Stop Recording")
        self.status_label.config(text="Recording...")
        self.result_label.config(text="")
        
        # Open audio stream
        self.stream = self.p.open(
            format=self.format,
            channels=self.channels,
            rate=self.rate,
            input=True,
            frames_per_buffer=self.chunk
        )
        
        # Start recording in a separate function
        self.root.after(10, self.record_frame)
    
    def record_frame(self):
        if self.recording:
            data = self.stream.read(self.chunk)
            self.frames.append(data)
            self.root.after(10, self.record_frame)
    
    def stop_recording(self):
        self.recording = False
        self.record_button.config(text="Start Recording")
        self.status_label.config(text="Processing...")
        
        # Stop and close the stream
        self.stream.stop_stream()
        self.stream.close()
        
        # Save the recorded audio
        audio_path = "audio_samples/recorded_korean.wav"
        wf = wave.open(audio_path, 'wb')
        wf.setnchannels(self.channels)
        wf.setsampwidth(self.p.get_sample_size(self.format))
        wf.setframerate(self.rate)
        wf.writeframes(b''.join(self.frames))
        wf.close()
        
        # Get the Korean word
        korean_word = self.word_entry.get().strip()
        if not korean_word:
            self.status_label.config(text="Please enter a Korean word!")
            return
        
        # Convert Korean text to romanized if needed
        if re.search(r'[가-힣]', korean_word):  # Check if contains Korean characters
            if korean_word in korean_to_roman:
                romanized_word = korean_to_roman[korean_word]
                self.status_label.config(text=f"Converting '{korean_word}' to '{romanized_word}'...")
            else:
                self.result_label.config(text=f"Korean word '{korean_word}' not in dictionary. Please use romanized version like 'pyeonuijeom'")
                self.status_label.config(text="Ready")
                return
        else:
            romanized_word = korean_word
        
        # Evaluate pronunciation
        try:
            result = self.api.evaluate_pronunciation(
                audio_path=audio_path,
                ref_text=romanized_word,
                core_type="word.eval.promax"
            )
            
            # Display results
            if isinstance(result, dict):
                if 'error' in result:
                    self.result_label.config(text=f"API Error: {result['error']}")
                else:
                    score = result.get('result', {}).get('overall', 0)
                    self.result_label.config(
                        text=f"Pronunciation Score: {score}/100\n"
                             f"Full result: {json.dumps(result, indent=2)}"
                    )
            else:
                self.result_label.config(text=f"Error: Unexpected response format\nResponse: {result}")
                
        except Exception as e:
            self.result_label.config(text=f"Error: {str(e)}")
        
        self.status_label.config(text="Ready")

if __name__ == "__main__":
    root = tk.Tk()
    app = KoreanRecorderApp(root)
    root.mainloop()
