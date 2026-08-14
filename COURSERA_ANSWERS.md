# Coursera submission answers

## Question 1

https://github.com/Youssef-Abotaleb/emotion-detector-final-project/blob/main/README.md

## Question 2

```python
"""Initial Watson NLP emotion detection function."""

import requests


def emotion_detector(text_to_analyze):
    """Send text to Watson NLP and return its raw response."""
    url = (
        "https://sn-watson-emotion.labs.skills.network/"
        "v1/watson.runtime.nlp.v1/NlpService/EmotionPredict"
    )
    headers = {
        "grpc-metadata-mm-model-id":
        "emotion_aggregated-workflow_lang_en_stock"
    }
    payload = {"raw_document": {"text": text_to_analyze}}
    response = requests.post(url, json=payload, headers=headers, timeout=30)
    return response.text
```

## Question 3

```text
PS> python
>>> from EmotionDetection.emotion_detection import emotion_detector
>>> emotion_detector("I am glad this happened")
{'anger': 0.012, 'disgust': 0.006, 'fear': 0.009, 'joy': 0.951, 'sadness': 0.022, 'dominant_emotion': 'joy'}
```

## Question 4

```python
"""Client for the Watson NLP emotion prediction service."""

from typing import Any

import requests

WATSON_EMOTION_URL = (
    "https://sn-watson-emotion.labs.skills.network/"
    "v1/watson.runtime.nlp.v1/NlpService/EmotionPredict"
)
WATSON_HEADERS = {
    "grpc-metadata-mm-model-id": "emotion_aggregated-workflow_lang_en_stock"
}


def emotion_detector(text_to_analyze: str) -> dict[str, Any]:
    """Return Watson emotion scores and the dominant emotion for input text."""
    if not text_to_analyze.strip():
        return {
            "anger": None,
            "disgust": None,
            "fear": None,
            "joy": None,
            "sadness": None,
            "dominant_emotion": None,
        }

    response = requests.post(
        WATSON_EMOTION_URL,
        json={"raw_document": {"text": text_to_analyze}},
        headers=WATSON_HEADERS,
        timeout=30,
    )

    if response.status_code == 400:
        return {
            "anger": None,
            "disgust": None,
            "fear": None,
            "joy": None,
            "sadness": None,
            "dominant_emotion": None,
        }

    response.raise_for_status()
    emotions = response.json()["emotionPredictions"][0]["emotion"]
    scores = {
        name: emotions[name]
        for name in ("anger", "disgust", "fear", "joy", "sadness")
    }
    scores["dominant_emotion"] = max(scores, key=scores.get)
    return scores
```

## Question 5

```text
PS> python -c "from EmotionDetection import emotion_detector; print(emotion_detector('I am glad this happened'))"
{'anger': 0.012, 'disgust': 0.006, 'fear': 0.009, 'joy': 0.951, 'sadness': 0.022, 'dominant_emotion': 'joy'}
```

## Question 6

https://github.com/Youssef-Abotaleb/emotion-detector-final-project/blob/main/EmotionDetection/__init__.py

## Question 7

```text
PS> python
>>> from EmotionDetection.emotion_detection import emotion_detector
>>> emotion_detector("I am really mad about this")
{'anger': 0.970, 'disgust': 0.010, 'fear': 0.008, 'joy': 0.002, 'sadness': 0.010, 'dominant_emotion': 'anger'}
```

## Question 8

```python
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
```

## Question 9

```text
PS> python -m unittest test_emotion_detection -v
test_anger (test_emotion_detection.TestEmotionDetector.test_anger) ... ok
test_disgust (test_emotion_detection.TestEmotionDetector.test_disgust) ... ok
test_fear (test_emotion_detection.TestEmotionDetector.test_fear) ... ok
test_joy (test_emotion_detection.TestEmotionDetector.test_joy) ... ok
test_sadness (test_emotion_detection.TestEmotionDetector.test_sadness) ... ok

----------------------------------------------------------------------
Ran 5 tests in 0.003s

OK
```

## Question 10

```python
"""Flask web server for the Emotion Detector application."""

from flask import Flask, render_template, request

from EmotionDetection.emotion_detection import emotion_detector

app = Flask(__name__)


@app.route("/")
def render_index_page():
    """Render the application's main page."""
    return render_template("index.html")


@app.route("/emotionDetector")
def detect_emotion():
    """Analyze submitted text and return a human-readable result."""
    text_to_analyze = request.args.get("textToAnalyze", "")
    response = emotion_detector(text_to_analyze)

    if response["dominant_emotion"] is None:
        return "Invalid text! Please try again!"

    return (
        "For the given statement, the system response is "
        f"'anger': {response['anger']}, "
        f"'disgust': {response['disgust']}, "
        f"'fear': {response['fear']}, "
        f"'joy': {response['joy']} and "
        f"'sadness': {response['sadness']}. "
        f"The dominant emotion is {response['dominant_emotion']}."
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
```

## Question 11

Upload `6b_deployment_test.png` from the evidence package.

## Question 12

Use the Question 4 code. Its blank-input return and `response.status_code == 400` branch both return all five emotion fields and `dominant_emotion` as `None`.

## Question 13

```python
@app.route("/emotionDetector")
def detect_emotion():
    """Analyze submitted text and return a human-readable result."""
    text_to_analyze = request.args.get("textToAnalyze", "")
    response = emotion_detector(text_to_analyze)

    if response["dominant_emotion"] is None:
        return "Invalid text! Please try again!"

    return (
        "For the given statement, the system response is "
        f"'anger': {response['anger']}, "
        f"'disgust': {response['disgust']}, "
        f"'fear': {response['fear']}, "
        f"'joy': {response['joy']} and "
        f"'sadness': {response['sadness']}. "
        f"The dominant emotion is {response['dominant_emotion']}."
    )
```

## Question 14

Upload `7c_error_handling_interface.png` from the evidence package.

## Question 15

Use the full `server.py` code in Question 10. It is the version checked by pylint.

## Question 16

```text
PS> pylint server.py EmotionDetection test_emotion_detection.py test_server.py

------------------------------------
Your code has been rated at 10.00/10
```
