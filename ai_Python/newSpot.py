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
scope = "playlist-read-private"

# Set up Spotify client with user authorization
spotify = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=spotify_client_id,
                                                   client_secret=spotify_client_secret,
                                                   redirect_uri=spotify_redirect_uri,
                                                   scope=scope))

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


def scrape_lyrics_from_web(artist, title, genius_access_token):
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
                lyrics_containers = soup.find_all("div", {"data-lyrics-container": "true"})
                lyrics = '\n'.join(container.get_text(separator='\n') for container in lyrics_containers if container)
                if lyrics:
                    return lyrics
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
        if track['track'] is not None:
            artist = track['track']['artists'][0]['name']
            title = track['track']['name']
            lyrics = scrape_lyrics_from_web(artist, title, genius_access_token)
            dataset.append({"Artist": artist, "Title": title, "Lyrics": lyrics})
        else:
            print("Encountered a track that is not accessible.")
    
    df = pd.DataFrame(dataset)
    df.to_csv('playlist_lyrics_dataset_big.csv', index=False)
    print("Dataset created successfully.")

if __name__ == "__main__":
    main()
