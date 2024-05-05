import pandas as pd

def load_data(filepath):
    return pd.read_csv(filepath)

def determine_overall_mood(data):
    # Ensure 'Moods' column entries are strings before attempting to split
    data['Moods'] = data['Moods'].apply(lambda x: x.split(', ') if isinstance(x, str) else [])
    # Expand the list of moods into separate rows
    all_moods = data.explode('Moods')
    # Group by song and count the frequency of each mood
    mood_counts = all_moods.groupby(['Artist', 'Title', 'Moods']).size().reset_index(name='Count')
    # Sort by count descending within each song
    mood_counts.sort_values(by=['Artist', 'Title', 'Count'], ascending=[True, True, False], inplace=True)
    # Take the top mood for each song
    overall_mood = mood_counts.drop_duplicates(subset=['Artist', 'Title']).set_index(['Artist', 'Title'])
    return overall_mood


def main():
    filepath = 'dataset_with_moods.csv'
    data = load_data(filepath)
    overall_mood = determine_overall_mood(data)
    print(overall_mood)

if __name__ == "__main__":
    main()
