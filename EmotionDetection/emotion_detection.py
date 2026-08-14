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
