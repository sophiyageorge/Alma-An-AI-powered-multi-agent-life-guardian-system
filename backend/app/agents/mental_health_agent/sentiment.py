"""
sentiment.py
Sentiment and emotion analysis logic.
"""

from textblob import TextBlob
from typing import Dict


def analyze_sentiment(text: str) -> Dict:
    """
    Analyze sentiment of given text.

    Args:
        text (str): Journal text

    Returns:
        Dict: mood_score and emotion label
    """
    try:
        blob = TextBlob(text)
        polarity = blob.sentiment.polarity

        if polarity > 0.3:
            emotion = "positive"
        elif polarity < -0.3:
            emotion = "negative"
        else:
            emotion = "neutral"

        return {
            "mood_score": round(polarity, 2),
            "emotion": emotion
        }

    except Exception as e:
        return {
            "mood_score": 0.0,
            "emotion": "unknown",
            "error": str(e)
        }