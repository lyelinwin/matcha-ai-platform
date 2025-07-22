import pandas as pd
from collections import Counter
from textblob import TextBlob

def load_social_data(filepath):
    """Load social media posts dataset"""
    return pd.read_csv(filepath)

def get_trending_drinks(df):
    """Find the most mentioned drinks in social posts"""
    all_text = " ".join(df["Text"].str.lower())
    drinks = [
        "matcha latte", "strawberry matcha latte", "mango coconut matcha",
        "honey lavender matcha", "iced vanilla matcha", "matcha lemonade", "matcha cold foam"
    ]
    drink_counts = {drink: all_text.count(drink) for drink in drinks}
    # Sort drinks by count (highest first)
    sorted_drinks = dict(sorted(drink_counts.items(), key=lambda x: x[1], reverse=True))
    return sorted_drinks

def load_social_data(filepath):
    """Load social media posts dataset"""
    return pd.read_csv(filepath)

def get_trending_drinks(df):
    """Find the most mentioned drinks in social posts"""
    all_text = " ".join(df["Text"].str.lower())
    drinks = [
        "matcha latte", "strawberry matcha latte", "mango coconut matcha",
        "honey lavender matcha", "iced vanilla matcha", "matcha lemonade", "matcha cold foam"
    ]
    drink_counts = {drink: all_text.count(drink) for drink in drinks}
    sorted_drinks = dict(sorted(drink_counts.items(), key=lambda x: x[1], reverse=True))
    return sorted_drinks

def analyze_sentiment(text):
    """Analyze the sentiment polarity of a post"""
    blob = TextBlob(text)
    polarity = blob.sentiment.polarity
    if polarity > 0:
        return "Positive"
    elif polarity < 0:
        return "Negative"
    else:
        return "Neutral"

def get_sentiment_summary(df):
    """Get sentiment counts for all posts"""
    df["Sentiment"] = df["Text"].apply(analyze_sentiment)
    sentiment_counts = df["Sentiment"].value_counts().to_dict()
    return sentiment_counts
