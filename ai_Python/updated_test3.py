import pandas as pd
import nltk
import re
from textblob import TextBlob
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize

# Ensure necessary NLTK data is downloaded
nltk.download('punkt')
nltk.download('stopwords')

# Load dataset from CSV
df = pd.read_csv('output_file1.csv')

# Function to expand contractions
def expand_contractions(text):
    contractions = {
        "can't": "cannot",
        "it's": "it is",
        "didn't": "did not",
        "I'm": "I am",
        "you're": "you are",
        "he's": "he is",
        "she's": "she is",
        "it's": "it is",
        "we're": "we are",
        "they're": "they are",
        "I've": "I have",
        "you've": "you have",
        "we've": "we have",
        "they've": "they have",
        "isn't": "is not",
        "aren't": "are not",
        "wasn't": "was not",
        "weren't": "were not",
        "hasn't": "has not",
        "haven't": "have not",
        "hadn't": "had not",
        "won't": "will not",
        "wouldn't": "would not",
        "don't": "do not",
        "doesn't": "does not",
        "didn't": "did not",
        "can't": "cannot",
        "couldn't": "could not",
        "shouldn't": "should not",
        "mightn't": "might not",
        "mustn't": "must not"
    }
    for key, value in contractions.items():
        text = text.replace(key, value)
    return text

# Enhanced cleaning function
def clean_lyrics(text):
    # Remove special characters
    text = re.sub(r'[^a-zA-Z0-9 ]', '', text)
    # Expand contractions
    text = expand_contractions(text)
    # Convert to lower case
    text = text.lower()
    return text.strip()

# Applying cleaning function
df['Cleaned_Lyrics'] = df['Lyrics'].apply(clean_lyrics)

# Sentiment analysis function
def preprocess_and_analyze_sentiment(lyrics):
    stop_words = set(stopwords.words('english'))
    sentences = sent_tokenize(lyrics)
    filtered_words = []
    for sentence in sentences:
        tokens = word_tokenize(sentence)
        filtered_words.extend([word for word in tokens if word.lower() not in stop_words and word.isalpha()])
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

# Emotion-color mapping
emotion_color_mapping = {
    'positive': 'yellow',
    'negative': 'dark blue',
    'neutral': 'grey'
}

# Apply color mapping to sentiments
def map_colors(sentiments):
    return [(word, sentiment, emotion_color_mapping.get(sentiment, 'grey')) for word, sentiment in sentiments]

df['Color_Mapping'] = df['Sentiments'].apply(map_colors)

# Save the final dataset to a new CSV
df.to_csv('processed_playlist_lyrics_dataset.csv', index=False)

print("Dataset processing complete and saved.")
