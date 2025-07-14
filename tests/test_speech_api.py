import unittest
import sys
import os
import json
from unittest.mock import patch, MagicMock

# Add the src directory to the path so we can import the speech_api module
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from speech_api import SuperSpeech

class TestSuperSpeech(unittest.TestCase):
    
    def setUp(self):
        """Set up test fixtures"""
        self.api = SuperSpeech(app_key="test_key", secret_key="test_secret")
    
    def test_init(self):
        """Test initialization with custom keys"""
        self.assertEqual(self.api.app_key, "test_key")
        self.assertEqual(self.api.secret_key, "test_secret")
        self.assertEqual(self.api.base_url, "https://api.speechsuper.com/")
        self.assertEqual(self.api.user_id, "guest")
    
    def test_generate_signatures(self):
        """Test signature generation"""
        timestamp = "1234567890"
        connect_sig, start_sig = self.api._generate_signatures(timestamp)
        
        # These expected values should match the hash algorithm in the API
        self.assertTrue(isinstance(connect_sig, str))
        self.assertTrue(isinstance(start_sig, str))
        self.assertEqual(len(connect_sig), 40)  # SHA-1 hash is 40 chars
    
    @patch('requests.post')
    def test_evaluate_pronunciation(self, mock_post):
        """Test pronunciation evaluation with mocked API response"""
        # Mock the API response
        mock_response = MagicMock()
        mock_response.text = json.dumps({
            "result": {
                "overall": 95,
                "pronunciation": 92,
                "words": [{"word": "test"}]
            }
        })
        mock_post.return_value = mock_response
        
        # Create a fake audio file path - the file doesn't need to exist for this test
        audio_path = "fake_audio.wav"
        
        # Mock the open function
        with patch('builtins.open', MagicMock()):
            result = self.api.evaluate_pronunciation(
                audio_path=audio_path,
                ref_text="test",
                core_type="word.eval.promax"
            )
        
        # Check the result
        self.assertEqual(result["result"]["overall"], 95)
        self.assertEqual(result["result"]["pronunciation"], 92)
        
        # Verify the API was called correctly
        mock_post.assert_called_once()
        args, kwargs = mock_post.call_args
        self.assertTrue(args[0].startswith("https://api.speechsuper.com/word.eval.promax"))

if __name__ == '__main__':
    unittest.main()
