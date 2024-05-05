import pandas as pd

def load_data(filepath):
    return pd.read_csv(filepath)

def aggregate_song_features(data):
    # Aggregate features across sections for each song
    aggregation_functions = {
        'Sentiment': 'mean',
        'Subjectivity': 'mean',
        'Tempo': 'mean',
        'Key': lambda x: x.mode()[0] if not x.mode().empty else x.iloc[0],
        'Loudness': 'mean',
        'Mode': lambda x: x.mode()[0] if not x.mode().empty else x.iloc[0]
    }
    full_song_features = data.groupby(['Artist', 'Title']).agg(aggregation_functions).reset_index()
    full_song_features.columns = [f'{col}_full' if col not in ['Artist', 'Title'] else col for col in full_song_features.columns]
    return full_song_features

def determine_overall_mood(data):
    # Handle empty moods by replacing empty lists with a placeholder
    data['Moods'] = data['Moods'].apply(lambda x: x.split(', ') if isinstance(x, str) else ['No Mood Tagged'])
    all_moods = data.explode('Moods')
    mood_counts = all_moods.groupby(['Artist', 'Title', 'Moods']).size().reset_index(name='Count')
    mood_counts.sort_values(by=['Artist', 'Title', 'Count'], ascending=[True, True, False], inplace=True)
    overall_mood = mood_counts.drop_duplicates(subset=['Artist', 'Title'])
    return overall_mood[['Artist', 'Title', 'Moods', 'Count']]

def combine_section_specific_features(data, full_song_features, overall_mood):
    combined_data = pd.merge(data, full_song_features, on=['Artist', 'Title'], how='left')
    # Merge the overall mood data
    combined_data = pd.merge(combined_data, overall_mood, on=['Artist', 'Title'], how='left')
    combined_data.rename(columns={'Moods': 'Overall_Mood', 'Count': 'Mood_Count'}, inplace=True)
    return combined_data

def main():
    filepath = 'dataset_with_big_moods.csv'
    output_filepath = 'average_big_mood_dataset.csv'
    data = load_data(filepath)
    full_song_features = aggregate_song_features(data)
    overall_mood = determine_overall_mood(data)
    combined_data = combine_section_specific_features(data, full_song_features, overall_mood)
    combined_data.to_csv(output_filepath, index=False)
    print("Dataset compiled successfully with overall mood and count.")

if __name__ == "__main__":
    main()
