import tkinter as tk
from tkinter import ttk
import pyaudio
import wave
import os
import json
import re
from src.speech_api import SuperSpeech
from hangul_romanize import Transliter
from hangul_romanize.rule import academic

# Instantiate the transliterator for automatic romanization
transliter = Transliter(academic)

class KoreanRecorderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Korean Pronunciation Tester")
        
        # Configure main window
        self.root.geometry("500x600")
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
        ttk.Label(self.root, text="Example: 남자 (namja) or 안녕 (annyeong) - Single words only!", font=('Arial', 8)).pack(pady=2)
        ttk.Label(self.root, text="Using Korean-specific API (word.eval.kr) - Audio limit: 20 seconds", font=('Arial', 7), foreground='blue').pack(pady=1)
        
        # Record button
        self.record_button = ttk.Button(
            self.root, 
            text="Start Recording",
            command=self.toggle_recording
        )
        self.record_button.pack(pady=20)
        
        # Playback button
        self.playback_button = ttk.Button(
            self.root, 
            text="Play Last Recording",
            command=self.play_recording,
            state="disabled"
        )
        self.playback_button.pack(pady=5)
        
        # Status label
        self.status_label = ttk.Label(self.root, text="")
        self.status_label.pack(pady=10)
        
        # Result label
        self.result_label = ttk.Label(self.root, text="", wraplength=450)
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
        
        # Enable playback button
        self.playback_button.config(state="normal")

        # Check if the recording is likely silent
        file_size = os.path.getsize(audio_path)
        if file_size < 20000:  # Heuristic: 20KB for a short word is generous
            self.result_label.config(text=f"Warning: Recorded audio is very small ({file_size} bytes).\n"
                                          "Please check if your microphone is working and not muted.\n"
                                          "Try speaking louder and closer to the microphone.")
            self.status_label.config(text="Ready")
            return
        
        # Get the Korean word
        korean_word = self.word_entry.get().strip()
        if not korean_word:
            self.status_label.config(text="Please enter a Korean word!")
            return
        
        # Automatically convert Korean text to romanized text
        if re.search(r'[가-힣]', korean_word):  # Check if contains Korean characters
            try:
                romanized_word = transliter.translit(korean_word)
                self.status_label.config(text=f"Converting '{korean_word}' to '{romanized_word}'...")
            except Exception as e:
                self.result_label.config(text=f"Could not romanize '{korean_word}': {e}")
                self.status_label.config(text="Ready")
                return
        else:
            romanized_word = korean_word
        
        # Add debugging info
        print(f"DEBUG: Audio file size: {file_size} bytes")
        print(f"DEBUG: Korean word: '{korean_word}'")
        print(f"DEBUG: Romanized word: '{romanized_word}'")
        print(f"DEBUG: Audio file saved to: {audio_path}")
        
        # Evaluate pronunciation
        try:
            # Use romanized text for the API call
            print(f"DEBUG: Trying API call with romanized text: '{romanized_word}'")
            
            # Check if it's a single word or multiple words
            word_count = len(romanized_word.split())
            if word_count == 1:
                # Single word - try Korean-specific word evaluation endpoints
                core_types_to_try = ["word.eval.kr", "word.eval.promax", "word.eval"]
                print(f"DEBUG: Using single word evaluation with Korean-specific core types")
            else:
                # Multiple words - inform user of limitation
                self.result_label.config(text=f"⚠️ Multi-word evaluation not available\n\n"
                                              f"Your API account supports Korean single word evaluation only.\n"
                                              f"Using core type: word.eval.kr (Audio limit: 20 seconds)\n\n"
                                              f"Please try individual words like:\n"
                                              f"• 남자 (namja)\n"
                                              f"• 커요 (keoyo)\n"
                                              f"• 사과 (sagwa)\n\n"
                                              f"You entered: '{korean_word}' → '{romanized_word}' ({word_count} words)")
                self.status_label.config(text="Ready")
                return
            
            result = None
            for core_type in core_types_to_try:
                try:
                    print(f"DEBUG: Trying core_type: {core_type}")
                    result = self.api.evaluate_pronunciation(
                        audio_path=audio_path,
                        ref_text=romanized_word,
                        core_type=core_type
                    )
                    print(f"DEBUG: API result for {core_type}: {result}")
                    
                    # If no error, break out of the loop
                    if result and not result.get('error'):
                        print(f"DEBUG: Success with {core_type}")
                        break
                    elif result and result.get('error'):
                        print(f"DEBUG: {core_type} failed with error: {result.get('error')}")
                        continue
                        
                except Exception as e:
                    print(f"DEBUG: Exception with {core_type}: {e}")
                    continue
            
            # If all attempts failed, show the last result
            if not result or result.get('error'):
                print(f"DEBUG: All core types failed. Last result: {result}")
                
        except Exception as e:
            print(f"DEBUG: Exception: {e}")
            self.result_label.config(text=f"Error: {str(e)}")
            self.status_label.config(text="Ready")
            return
            
        # Display results with detailed metrics
        print(f"DEBUG: Final result to display: {result}")
        if isinstance(result, dict):
            if 'error' in result:
                self.result_label.config(text=f"API Error: {result['error']}\n"
                                              f"Core type attempted: {core_type if 'core_type' in locals() else 'Unknown'}")
            else:
                # Extract detailed metrics from the result
                res = result.get('result', {})
                overall_score = res.get('overall', 0)
                pronunciation_score = res.get('pronunciation', 0)
                fluency_score = res.get('fluency', 0)
                rhythm_score = res.get('rhythm', 0)
                speed_wpm = res.get('speed', 0)
                integrity_score = res.get('integrity', 0)
                duration = res.get('duration', '0')
                
                # Create a detailed results display
                result_text = f"🎯 Overall Score: {overall_score}/100\n\n"
                
                # Main metrics
                result_text += f"📊 Detailed Scores:\n"
                result_text += f"• Pronunciation: {pronunciation_score}/100\n"
                result_text += f"• Fluency: {fluency_score}/100\n"
                result_text += f"• Rhythm: {rhythm_score}/100\n"
                result_text += f"• Integrity: {integrity_score}/100\n"
                result_text += f"• Speed: {speed_wpm} WPM\n"
                result_text += f"• Duration: {duration}s\n\n"
                
                # Word-by-word analysis
                words = res.get('words', [])
                if words:
                    result_text += f"📝 Word Analysis:\n"
                    for i, word in enumerate(words):
                        word_text = word.get('word', f'Word {i+1}')
                        word_score = word.get('scores', {}).get('overall', 0)
                        word_pronunciation = word.get('scores', {}).get('pronunciation', 0)
                        result_text += f"• {word_text}: {word_score}/100 (pronunciation: {word_pronunciation}/100)\n"
                    result_text += "\n"
                
                # Audio info
                result_text += f"🔊 Audio: {audio_path} ({file_size} bytes)\n"
                result_text += f"📝 Text: '{korean_word}' → '{romanized_word}'\n"
                result_text += f"⚙️ Core Type: {core_type if 'core_type' in locals() else 'sent.eval.promax'}"
                
                self.result_label.config(text=result_text)
        else:
            self.result_label.config(text=f"Error: Unexpected response format\nResponse: {result}")
        
        self.status_label.config(text="Ready")

    def play_recording(self):
        """Play back the last recorded audio file"""
        audio_path = "audio_samples/recorded_korean.wav"
        abs_audio_path = os.path.abspath(audio_path)
        
        print(f"DEBUG: Trying to play: {abs_audio_path}")
        print(f"DEBUG: File exists: {os.path.exists(abs_audio_path)}")
        
        if os.path.exists(abs_audio_path):
            try:
                import subprocess
                import platform
                
                system = platform.system()
                if system == "Windows":
                    # Try multiple methods for Windows
                    try:
                        # Method 1: Use os.startfile with absolute path
                        os.startfile(abs_audio_path)
                        self.status_label.config(text="Playing recording with default app...")
                    except Exception as e1:
                        try:
                            # Method 2: Use subprocess with start command
                            subprocess.run(["start", "", abs_audio_path], shell=True, check=True)
                            self.status_label.config(text="Playing recording with start command...")
                        except Exception as e2:
                            try:
                                # Method 3: Try with Windows Media Player
                                subprocess.run(["wmplayer", abs_audio_path], check=True)
                                self.status_label.config(text="Playing recording with Windows Media Player...")
                            except Exception as e3:
                                # Show all error details
                                self.result_label.config(text=f"Could not play audio:\n"
                                                              f"Method 1 (startfile): {e1}\n"
                                                              f"Method 2 (start): {e2}\n"
                                                              f"Method 3 (wmplayer): {e3}")
                                return
                elif system == "Darwin":  # macOS
                    subprocess.run(["open", abs_audio_path])
                    self.status_label.config(text="Playing recording...")
                else:  # Linux
                    subprocess.run(["xdg-open", abs_audio_path])
                    self.status_label.config(text="Playing recording...")
                    
                self.root.after(3000, lambda: self.status_label.config(text="Ready"))
            except Exception as e:
                self.result_label.config(text=f"Could not play audio: {e}\nFile path: {abs_audio_path}")
        else:
            self.result_label.config(text=f"No recording found at: {abs_audio_path}\nRecord something first!")

if __name__ == "__main__":
    root = tk.Tk()
    app = KoreanRecorderApp(root)
    root.mainloop()
