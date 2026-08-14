# Emotion Detector

Emotion Detector is the final project for the IBM *Developing AI Applications with Python and Flask* course. It sends English text to the Watson NLP Emotion Predict service and returns anger, disgust, fear, joy, sadness, and the dominant emotion.

## Run locally

```bash
python -m pip install -r requirements.txt
python server.py
```

Open `http://localhost:5000`, enter a sentence, and select **Run Emotion Detection**.

## Verify

```bash
python -m unittest discover -v
pylint server.py EmotionDetection
```

The `evidence/` directory contains the code and terminal-output captures requested by the Coursera rubric.
