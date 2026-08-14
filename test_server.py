"""Tests for Flask deployment and blank-input error handling."""

import unittest
from unittest.mock import patch

from server import app


class TestServer(unittest.TestCase):
    """Verify the web endpoint formats success and error responses."""

    def setUp(self):
        """Create a Flask test client."""
        self.client = app.test_client()

    def test_blank_input(self):
        """Blank text should display the required validation message."""
        response = self.client.get("/emotionDetector?textToAnalyze=")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.text, "Invalid text! Please try again!")

    @patch("server.emotion_detector")
    def test_formatted_result(self, detector):
        """A successful analysis should include its dominant emotion."""
        detector.return_value = {
            "anger": 0.01,
            "disgust": 0.01,
            "fear": 0.01,
            "joy": 0.96,
            "sadness": 0.01,
            "dominant_emotion": "joy",
        }
        response = self.client.get("/emotionDetector?textToAnalyze=I+am+happy")
        self.assertEqual(response.status_code, 200)
        self.assertIn("The dominant emotion is joy.", response.text)


if __name__ == "__main__":
    unittest.main()
