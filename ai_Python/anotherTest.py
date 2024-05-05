import pandas as pd
import re
import nltk

nltk.download('words')
from nltk.corpus import words
english_words = set(words.words())

# Define a simple list of English stopwords
simple_stopwords = set([
    "i", "me", "my", "myself", "we", "our", "ours", "ourselves", "you", "your", "yours",
    "yourself", "yourselves", "he", "him", "his", "himself", "she", "her", "hers",
    "herself", "it", "its", "itself", "they", "them", "their", "theirs", "themselves",
    "what", "which", "who", "whom", "this", "that", "these", "those", "am", "is", "are",
    "was", "were", "be", "been", "being", "have", "has", "had", "having", "do", "does",
    "did", "doing", "a", "an", "the", "and", "but", "if", "or", "because", "as", "until",
    "while", "of", "at", "by", "for", "with", "about", "against", "between", "into",
    "through", "during", "before", "after", "above", "below", "to", "from", "up", "down",
    "in", "out", "on", "off", "over", "under", "again", "further", "then", "once", "here",
    "there", "when", "where", "why", "how", "all", "any", "both", "each", "few", "more",
    "most", "other", "some", "such", "no", "nor", "not", "only", "own", "same", "so",
    "than", "too", "very", "s", "t", "can", "will", "just", "don", "should", "now"
])

# Function to expand contractions
def expand_contractions(text):
    contractions = {
        "can't": "cannot",
        "it's": "it is",
        "didn't": "did not",
        "i'm": "i am",
        "you're": "you are",
        "he's": "he is",
        "she's": "she is",
        "we're": "we are",
        "they're": "they are",
        "i've": "i have",
        "you've": "you have",
        "we've": "we have",
        "they've": "they have",
        "isn't": "is not",
        "aren't": "are not",
        "wasn't": "was not",
        "weren't": "were not",
        "they'd": "they would",
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

    # Pattern to match word boundaries
    pattern = re.compile(r'\b(' + '|'.join(contractions.keys()) + r')\b', flags=re.IGNORECASE)

    # Function to replace match with corresponding value in dictionary
    def replace(match):
        return contractions[match.group(0).lower()]

    return pattern.sub(replace, text)

    # Old contraction code
    """for key, value in contractions.items():
        text = text.replace(key, value)
    return text"""


def clean_lyrics(text):
    # Expand contractions first
    text = expand_contractions(text)

    # Convert to lowercase
    text = text.lower()

    # Remove unwanted phrases or patterns
    text = re.sub(r'\bla[-\s]*la[-\s]*la[-\s]*la\b|\boh\sna\sna\sna\b', '', text)

    # Remove special characters, preserving intra-word apostrophes
    text = re.sub(r'(?<!\w)[^\s\w]+|[^\s\w]+(?!\w)', '', text)

    # Split text into lines
    lines = text.split('\n')

    # Process each line
    cleaned_lines = []
    for line in lines:
        # Remove stopwords
        words = line.split()
        words = [word for word in words if word not in simple_stopwords and word in english_words]

        # Reconstruct the line
        processed_line = ' '.join(words)
        if processed_line:
            cleaned_lines.append(processed_line)
    
    return cleaned_lines


# Load the CSV
df = pd.read_csv('playlist_lyrics_dataset.csv')

# Create an empty list to store processed lyrics
all_processed_lyrics = []

# Iterate over each row in the DataFrame
for index, row in df.iterrows():
    lyrics = row['Lyrics']
    processed_lyrics = clean_lyrics(lyrics)
    all_processed_lyrics.extend(processed_lyrics)

# Create a new DataFrame with each line as a row
new_df = pd.DataFrame(all_processed_lyrics, columns=['Cleaned Lyrics'])

# Save the new DataFrame to a CSV
output_path = 'output_file1.csv'
new_df.to_csv(output_path, index=False)

print("All lyrics have been processed and saved to a new CSV file.")