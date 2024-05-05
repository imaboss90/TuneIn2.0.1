import spotipy
from spotipy.oauth2 import SpotifyOAuth
import lyricsgenius
import pandas as pd

# Spotify credentials
spotify_client_id = 'd5e0b694dd004aba830a5e676047cc85'
spotify_client_secret = '2dfd94a1d3104f9faa0666432b6f8166'
spotify_redirect_uri = 'http://localhost:8080/'

# Genius credentials
genius_access_token = 'RwSuDcRFDRzcdL-UOFd6-QjVFT6B5dV-Hy6VU5M6fn1Anuqc1EOtKK2sgJtLhAMD'

# Scopes for Spotify authorization
scope = "playlist-read-private"

# Set up Spotify client with user authorization
spotify = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=spotify_client_id,
                                                    client_secret=spotify_client_secret,
                                                    redirect_uri=spotify_redirect_uri,
                                                    scope=scope))

# Set up Genius client
genius = lyricsgenius.Genius(genius_access_token)

def get_playlist_tracks(playlist_id):
    try:
        results = spotify.playlist_tracks(playlist_id)
        tracks = results['items']
        while results['next']:
            results = spotify.next(results)
            tracks.extend(results['items'])
        return tracks
    except Exception as e:
        print(f"Error accessing playlist: {e}")
        return []

def get_lyrics(artist, title):
    try:
        song = genius.search_song(title, artist)
        if song:
            return song.lyrics
    except Exception as e:
        print(f"Error fetching lyrics for {title} by {artist}: {e}")
    return "Lyrics Not Found"

def main():
    playlist_url = input("Enter the Spotify playlist URL or ID: ")
    playlist_id = playlist_url.split("playlist/")[1].split("?")[0]  # Extracting the playlist ID from the URL

    tracks = get_playlist_tracks(playlist_id)
    
    if not tracks:
        print("No tracks found in the playlist or unable to access the playlist.")
        return
    
    dataset = []
    
    for track in tracks:
        # Check if the track object is not None
        if track['track'] is not None:
            artist = track['track']['artists'][0]['name']
            title = track['track']['name']
            lyrics = get_lyrics(artist, title)
            dataset.append({"Artist": artist, "Title": title, "Lyrics": lyrics})
        else:
            # Handle the case where the track is None
            print("Encountered a track that is not accessible.")
    
    # Convert to DataFrame
    df = pd.DataFrame(dataset)
    
    # Export to CSV
    df.to_csv('playlist_lyrics_dataset_dua.csv', index=False)
    print("Dataset created successfully.")


if __name__ == "__main__":
    main()
