# SuperSpeech Korean Pronunciation Tester

A Python application for Korean pronunciation assessment using the SpeechSuper API. This tool provides real-time pronunciation scoring for both individual Korean words and sentences.

## Features

- 🎤 **Audio Recording**: Built-in microphone recording with 16kHz quality
- 🇰🇷 **Korean Language Support**: Automatic Korean-to-romanized text conversion
- 📊 **Detailed Scoring**: Comprehensive pronunciation analysis including:
  - Overall pronunciation score
  - Pronunciation accuracy
  - Fluency assessment
  - Rhythm analysis
  - Speech integrity
  - Words-per-minute calculation
- 🔄 **Dual API Support**: 
  - Single words: `word.eval.kr`
  - Sentences/phrases: `sent.eval.kr`
- 🎵 **Audio Playback**: Review your recordings before evaluation
- 🔒 **Secure Configuration**: API keys stored in environment variables

- **Word Pronunciation Assessment**: Evaluate pronunciation at the word level with detailed phonetic analysis
- **Sentence Evaluation**: Assess fluency, stress patterns, and intonation in full sentences
- **Spontaneous Speech Analysis**: Evaluate unscripted speech with grammar, vocabulary, and relevance scoring
- **Simple Python API**: Easy-to-use Python wrapper around the SpeechSuper API

## Installation

Clone this repository to get started:

`ash
git clone https://github.com/ohcrapitsmrtee/SuperSpeech.git
cd SuperSpeech
pip install -r requirements.txt
`

## Quick Start

`python
from src.speech_api import SuperSpeech

# Initialize the API with your credentials
api = SuperSpeech(
    app_key="your_app_key",
    secret_key="your_secret_key"
)

# Evaluate word pronunciation
result = api.evaluate_pronunciation(
    audio_path="audio_samples/supermarket.wav",
    ref_text="supermarket",
    core_type="word.eval.promax"
)

print(f"Pronunciation score: {result['result']['pronunciation']}")
print(f"Overall score: {result['result']['overall']}")
`

## API Reference

### SuperSpeech Class

The main class for interacting with the SpeechSuper API.

#### Methods

- **evaluate_pronunciation(audio_path, ref_text, core_type="word.eval.promax", audio_type="wav", audio_sample_rate=16000)**
  
  Evaluate pronunciation of words or sentences.

- **evaluate_spontaneous_speech(audio_path, question_prompt, test_type="ielts", model="non_native", penalize_offtopic=1, audio_type="wav", audio_sample_rate=16000)**
  
  Evaluate spontaneous speech with various metrics.

## Audio Requirements

For optimal results, prepare audio files with these specifications:

| Audio Attribute | Recommendation |
|----------------|---------------|
| Sample size    | 16-bit        |
| Sample rate    | 16kHz         |
| Channels       | 1 (mono)      |
| Format         | WAV, MP3, OGG |

## Example Applications

Check the src/example.py file for usage examples.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Based on [SpeechSuper API Samples](https://github.com/speechsuper/speechsuper-api-samples)
- Thanks to SpeechSuper for their pronunciation assessment API
