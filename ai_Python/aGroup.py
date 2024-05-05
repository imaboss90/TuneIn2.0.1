import pandas as pd
import re
from textblob import TextBlob
from transformers import pipeline

# Load a pre-trained sentiment analysis model
model_name = "nlptown/bert-base-multilingual-uncased-sentiment"
sentiment_model = pipeline("sentiment-analysis", model=model_name)

def analyze_sentiment(lyrics):
    result = sentiment_model(lyrics)
    # The model returns a list of dictionaries with 'label' and 'score'
    label = result[0]['label']
    score = result[0]['score']
    return label, score

def read_lyrics_data(filepath):
    try:
        return pd.read_csv(filepath)
    except FileNotFoundError:
        print("Error: The specified file was not found.")
        return None
    except pd.errors.EmptyDataError:
        print("Error: The file is empty.")
        return None

def group_lyrics_by_section(lyrics_text):
    sections = {}
    current_section = None
    lyrics_parts = re.split(r'(\[.*?\])', lyrics_text)

    for part in lyrics_parts:
        if re.match(r'\[.*?\]', part):
            current_section = part.strip()
            sections[current_section] = []
        elif current_section:
            sections[current_section].append(part.strip())

    for section, lines in sections.items():
        sections[section] = ' '.join(lines).strip()

    return sections

def analyze_sentiment(lyrics):
    analysis = TextBlob(lyrics)
    return analysis.sentiment.polarity, analysis.sentiment.subjectivity

def process_lyrics_data(data):
    rows = []
    for index, row in data.iterrows():
        if pd.notna(row['Lyrics']):
            processed_lyrics = group_lyrics_by_section(row['Lyrics'])
            for section, lyrics in processed_lyrics.items():
                sentiment, subjectivity = analyze_sentiment(lyrics)
                rows.append([row['Artist'], row['Title'], section, lyrics, sentiment, subjectivity])
    return pd.DataFrame(rows, columns=['Artist', 'Title', 'Section', 'Lyrics', 'Sentiment', 'Subjectivity'])

def save_data_to_csv(data, filename):
    data.to_csv(filename, index=False)
    print(f"Dataset saved successfully to {filename}.")

    #"Tempo": audio_features['tempo'],"Key": audio_features['key'],"Loudness": audio_features['loudness'],"Mode": audio_features['mode']

def main():
    input_filepath = 'playlist_lyrics_dataset_big.csv'
    output_filepath = 'version_big_lyrics_sentiment.csv'

    input_filepath_audio = 'playlist_lyrics_big_audio_features.csv'
    

    data = read_lyrics_data(input_filepath)
    data_audio = read_lyrics_data(input_filepath_audio)
    
    selected_columns = ['Artist', 'Title', 'Tempo', 'Key', 'Loudness', 'Mode']
    
    if data is not None:
        processed_data = process_lyrics_data(data)
        merged_data = pd.merge(processed_data, data_audio[selected_columns], how='left')
        save_data_to_csv(merged_data, output_filepath)

if __name__ == "__main__":
    main()
