import pandas as pd
import nltk
import re
from textblob import TextBlob
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

# Download necessary NLTK data
nltk.download('punkt')
nltk.download('stopwords')

# Define the enhanced cleaning function
def clean_lyrics(text):
    # Remove lines that may contain metadata like "X ContributorsTranslations..."
    text = re.sub(r'\d+ Contributors.*?\n', '', text)
    # Attempt to remove any standalone numbers and isolated non-lyrical phrases that might be metadata
    text = re.sub(r'\b\d+\b', '', text)  # Remove isolated numbers
    text = re.sub(r'Translations.*', '', text)  # Assume anything after 'Translations' is not lyrics
    # General cleanup for leading/trailing whitespace and excessive whitespace within text
    text = re.sub(r'\s+', ' ', text).strip()
    return text

# Load your dataset
df = pd.read_csv('playlist_lyrics_dataset.csv')

# Clean the lyrics
df['Cleaned_Lyrics'] = df['Lyrics'].apply(clean_lyrics)

# Function to preprocess and analyze sentiment
def preprocess_and_analyze_sentiment(lyrics):
    # Tokenize and remove stop words
    stop_words = set(stopwords.words('english'))
    tokens = word_tokenize(lyrics)
    filtered_words = [word for word in tokens if word.lower() not in stop_words and word.isalpha()]
    # Analyze sentiment of each word using TextBlob
    sentiments = []
    for word in filtered_words:
        blob = TextBlob(word)
        sentiment_polarity = blob.sentiment.polarity
        if sentiment_polarity > 0:
            sentiment = 'positive'
        elif sentiment_polarity < 0:
            sentiment = 'negative'
        else:
            sentiment = 'neutral'
        sentiments.append((word, sentiment))
    return sentiments

# Apply the function to cleaned lyrics
df['Sentiments'] = df['Cleaned_Lyrics'].apply(preprocess_and_analyze_sentiment)

# Expanding sentiments into a new DataFrame
expanded_sentiments_list = []
for index, sentiments in enumerate(df['Sentiments']):
    expanded_sentiments_list.extend([(index, *t) for t in sentiments])

sentiments_expanded = pd.DataFrame(expanded_sentiments_list, columns=['Index', 'Word', 'Sentiment'])

# Define your emotion-color mapping
emotion_color_mapping = {
    'positive': 'yellow',
    'negative': 'dark blue',
    'neutral': 'beige',
    'happiness': 'yellow',
    'sadness': 'blue',
    'anger': 'red',
    'fear': 'black',
    'surprise': 'orange',
    'anticipation': 'magenta',
    'trust': 'green',
    'disgust': 'brown'
}

# Map sentiments to colors
sentiments_expanded['Color'] = sentiments_expanded['Sentiment'].map(emotion_color_mapping)

# Select the relevant columns for the final dataset
final_dataset = sentiments_expanded[['Word', 'Sentiment', 'Color']]

# Save the final dataset to CSV
final_dataset.to_csv('lyrics_sentiment_color_dataset.csv', index=False)

print("Dataset created successfully.")
