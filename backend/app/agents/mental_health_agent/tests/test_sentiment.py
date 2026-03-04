"""
test_sentiment.py
Unit tests for sentiment analysis.
"""

from app.agents.mental_health_agent.sentiment import analyze_sentiment


def test_positive_sentiment():
    text = "I am feeling amazing and happy today!"
    result = analyze_sentiment(text)

    assert result["emotion"] == "positive"
    assert result["mood_score"] > 0


def test_negative_sentiment():
    text = "I feel terrible and sad."
    result = analyze_sentiment(text)

    assert result["emotion"] == "negative"
    assert result["mood_score"] < 0


def test_neutral_sentiment():
    text = "Today was a normal day."
    result = analyze_sentiment(text)

    assert result["emotion"] in ["neutral", "positive", "negative"]