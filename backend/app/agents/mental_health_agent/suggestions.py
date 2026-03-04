"""
suggestions.py
Activity and reading suggestions.
"""

def suggest_activity(emotion: str) -> dict:
    """
    Suggest activity based on detected emotion.
    """
    suggestions = {
        "negative": {
            "activity": "5-minute breathing exercise",
            "reading": "Short motivational article"
        },
        "neutral": {
            "activity": "Gratitude journaling",
            "reading": "Mindfulness tips"
        },
        "positive": {
            "activity": "Light workout or walk",
            "reading": "Growth mindset article"
        }
    }

    return suggestions.get(emotion, {})