import pandas as pd

def star_to_sentiment(stars):
    # Map from 1-5 stars to a scale from -1 to 1
    return (stars - 3) / 2

def assign_mood(sentiment, tempo, loudness, mode):
    moods = []
    # Energizing and Upbeat conditions
    if tempo > 120:
        if loudness > -8:
            moods.append('Energetic')
            if sentiment > 0.5:
                moods.extend(['Joyous', 'Uplifting'])
            elif 0.2 < sentiment <= 0.5:
                moods.extend(['Happy', 'Excited'])
        else:
            moods.append('Laid Back')
        if sentiment < -0.1:
            moods.extend(['Aggressive', 'Intense'])
            if loudness > -5:
                moods.append('Fiery')

    # Calm and Serene conditions
    else:
        if mode == 0:  # Minor key
            if sentiment < -0.5:
                moods.extend(['Melancholic', 'Sad', 'Mournful'])
            elif -0.5 <= sentiment < -0.2:
                moods.extend(['Emotional', 'Reflective'])
            else:
                moods.append('Calm')
        if mode == 1:  # Major key
            if sentiment > 0.5:
                moods.extend(['Serene', 'Contented', 'Peaceful'])
            elif 0.2 < sentiment <= 0.5:
                moods.extend(['Optimistic', 'Relaxed'])

    return moods

# Load your dataset
dataset = pd.read_csv("version_bert_lyrics_sentiment.csv")  # Assume this is the correct CSV with BERT output

# Iterate over each row in the dataset
for index, row in dataset.iterrows():
    # Convert star rating to sentiment score
    sentiment_score = star_to_sentiment(int(row['Sentiment']))

    # Extract relevant features for the current song
    tempo = row['Tempo']
    loudness = row['Loudness']
    mode = row['Mode']
    
    # Apply assign_mood function to the features
    moods = assign_mood(sentiment_score, tempo, loudness, mode)
    
    # Update the dataset with the calculated moods
    dataset.at[index, 'Moods'] = ', '.join(moods)

# Save the updated dataset with moods
dataset.to_csv("dataset_with_bert_moods.csv", index=False)
