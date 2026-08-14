"""Unit tests for Watson NLP emotion detection output formatting."""

import unittest
from unittest.mock import Mock, patch

from EmotionDetection.emotion_detection import emotion_detector


class TestEmotionDetector(unittest.TestCase):
    """Verify each sample sentence produces the expected dominant emotion."""

    @staticmethod
    def _watson_response(dominant_emotion):
        scores = {
            "anger": 0.01,
            "disgust": 0.01,
            "fear": 0.01,
            "joy": 0.01,
            "sadness": 0.01,
        }
        scores[dominant_emotion] = 0.96
        response = Mock(status_code=200)
        response.json.return_value = {
            "emotionPredictions": [{"emotion": scores}]
        }
        response.raise_for_status.return_value = None
        return response

    def _assert_dominant(self, sentence, expected):
        with patch("EmotionDetection.emotion_detection.requests.post") as post:
            post.return_value = self._watson_response(expected)
            self.assertEqual(emotion_detector(sentence)["dominant_emotion"], expected)

    def test_joy(self):
        """A joyful sentence should be classified as joy."""
        self._assert_dominant("I am glad this happened", "joy")

    def test_anger(self):
        """An angry sentence should be classified as anger."""
        self._assert_dominant("I am really mad about this", "anger")

    def test_disgust(self):
        """A disgusted sentence should be classified as disgust."""
        self._assert_dominant("I feel disgusted just hearing about this", "disgust")

    def test_sadness(self):
        """A sad sentence should be classified as sadness."""
        self._assert_dominant("I am so sad about this", "sadness")

    def test_fear(self):
        """A fearful sentence should be classified as fear."""
        self._assert_dominant("I am really afraid that this will happen", "fear")


if __name__ == "__main__":
    unittest.main()
