import spotipy
from spotipy.oauth2 import SpotifyOAuth
import pandas as pd
import requests
from bs4 import BeautifulSoup


# Spotify credentials
spotify_client_id = 'd5e0b694dd004aba830a5e676047cc85'
spotify_client_secret = '2dfd94a1d3104f9faa0666432b6f8166'
spotify_redirect_uri = 'http://localhost:8080/'

# Genius credentials
genius_access_token = 'RwSuDcRFDRzcdL-UOFd6-QjVFT6B5dV-Hy6VU5M6fn1Anuqc1EOtKK2sgJtLhAMD'

# Scopes for Spotify authorization
scope = "playlist-read-private user-library-read"

# Set up Spotify client with user authorization
spotify = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=spotify_client_id,
                                                   client_secret=spotify_client_secret,
                                                   redirect_uri=spotify_redirect_uri,
                                                   scope=scope))

# Function to get playlist tracks
def get_playlist_tracks(playlist_id):
    results = spotify.playlist_tracks(playlist_id)
    tracks = results['items']
    while results['next']:
        results = spotify.next(results)
        tracks.extend(results['items'])
    return tracks

# Function to scrape lyrics from web
def scrape_lyrics_from_web(artist, title):
    query = f"{title} {artist}".replace(' ', '%20')
    search_url = f"https://api.genius.com/search?q={query}"
    headers = {"Authorization": f"Bearer {genius_access_token}"}
    response = requests.get(search_url, headers=headers)
    json_response = response.json()
    if 'hits' in json_response['response'] and json_response['response']['hits']:
        for hit in json_response['response']['hits']:
            if artist.lower() in hit['result']['primary_artist']['name'].lower():
                song_url = hit['result']['url']
                page_response = requests.get(song_url)
                html = page_response.text
                soup = BeautifulSoup(html, 'html.parser')
                lyrics_div = soup.find("div", class_="lyrics") or soup.find("div", attrs={"data-lyrics-container": "true"})
                lyrics = lyrics_div.get_text(separator="\n") if lyrics_div else "Lyrics Not Found"
                return lyrics
    return "Lyrics Not Found"

# Function to fetch audio features
def get_audio_features(track_id):
    return spotify.audio_features([track_id])[0]

# Main function
def main():
    playlist_url = input("Enter the Spotify playlist URL or ID: ")
    playlist_id = playlist_url.split("playlist/")[1].split("?")[0]

    tracks = get_playlist_tracks(playlist_id)
    dataset = []

    for track in tracks:
        if track['track'] is not None:
            artist = track['track']['artists'][0]['name']
            title = track['track']['name']
            track_id = track['track']['id']
            lyrics = scrape_lyrics_from_web(artist, title)
            audio_features = get_audio_features(track_id)
            dataset.append({
                "Artist": artist,
                "Title": title,
                "Lyrics": lyrics,
                "Tempo": audio_features['tempo'],
                "Key": audio_features['key'],
                "Loudness": audio_features['loudness'],
                "Mode": audio_features['mode']
            })

    df = pd.DataFrame(dataset)
    df.to_csv('playlist_lyrics_big_audio_features.csv', index=False)
    print("Dataset created successfully with audio features.")

if __name__ == "__main__":
    main()
