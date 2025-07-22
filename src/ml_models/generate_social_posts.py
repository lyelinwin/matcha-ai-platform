import pandas as pd 
import random

# drinks from forecast menu
drinks = [ "Matcha Latte", "Strawberry Matcha Latte", "Mango Coconut Matcha", "Honey Lavender Matcha", "Iced Vanilla Matcha", "Matcha Lemonade", "Matcha Cold Foam"]

# sentiment phrases
positive_phrases = [
    "I love", "Absolutely obsessed with", "Highly recommend", 
    "This is my new favorite", "So refreshing!", "Delicious and perfect for summer"
]
negative_phrases = [
    "Not a fan of", "Wouldn't recommend", "Too sweet for me", 
    "This didn’t work for me", "Disappointed with"
]
neutral_phrases = [
    "Tried", "Just had", "Anyone else tried", "Got the", "Thinking about ordering"
]

# hashtags
hashtags = ["#matcha", "#matchalatte", "#matchalover", "#icedmatcha", "#matchareview"]

# generating fake posts
posts = []
for i in range(1, 501):  # 500 posts
    drink = random.choice(drinks)
    sentiment_type = random.choices(
        ["positive", "negative", "neutral"], weights=[0.6, 0.2, 0.2]
    )[0]
    
    if sentiment_type == "positive":
        phrase = random.choice(positive_phrases)
    elif sentiment_type == "negative":
        phrase = random.choice(negative_phrases)
    else:
        phrase = random.choice(neutral_phrases)
    
    hashtags_sample = " ".join(random.sample(hashtags, k=2))
    text = f"{phrase} {drink}! {hashtags_sample}"
    
    posts.append([i, text])

# saving to CSV
social_df = pd.DataFrame(posts, columns=["PostID", "Text"])
social_df.to_csv("data/social_posts.csv", index=False)

print("social_posts.csv with 500 realistic posts created!")