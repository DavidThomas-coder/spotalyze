import os
import requests
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

SPOTIFY_CLIENT_ID = os.getenv('SPOTIFY_CLIENT_ID')
SPOTIFY_CLIENT_SECRET = os.getenv('SPOTIFY_CLIENT_SECRET')


def access_token():
    try:
        auth_url = "https://accounts.spotify.com/api/token"
        auth_response = requests.post(auth_url, {
            'grant_type': 'client_credentials',
            'client_id': SPOTIFY_CLIENT_ID,
            'client_secret': SPOTIFY_CLIENT_SECRET,
        })
        auth_response_data = auth_response.json()
        token = auth_response_data.get('access_token')
        if not token:
            print(f"Error obtaining access token: {auth_response_data}")
            return None
        return token
    except Exception as e:
        print(f"Error obtaining access token: {e}")
        return None

def extract_top_tracks(access_token):
    try:
        url = "https://api.spotify.com/v1/playlists/37i9dQZEVXbMDoHDwVN2tF/tracks"  # Spotify's Top 50 Global playlist
        headers = {
            "Authorization": f"Bearer {access_token}"
        }
        response = requests.get(url, headers=headers)
        data = response.json()
        print(f"Raw data: {data}")  # Inspect the raw data structure
        return data
    except Exception as e:
        print(f"Error fetching top tracks: {e}")
        return None

def transform_data(data):
    try:
        if 'items' not in data:
            raise ValueError("Unexpected data format: 'items' key not found")
        
        tracks = data['items']
        track_data = []
        for item in tracks:
            track = item['track']
            track_info = {
                'id': track.get('id'),
                'name': track.get('name'),
                'artists': ", ".join(artist['name'] for artist in track.get('artists', [])),
                'album': track.get('album', {}).get('name'),
                'release_date': track.get('album', {}).get('release_date'),
                'popularity': track.get('popularity')
            }
            track_data.append(track_info)

        df = pd.DataFrame(track_data)
        return df
    except Exception as e:
        print(f"Error transforming data: {e}")
        return None

def save_data_locally(data, filename_prefix="spotify_top_songs"):
    """Save data to a local JSON file."""
    today = date.today()
    filename = f"{filename_prefix}_{today}.json"
    pd.concat(data).to_json(filename, orient='records')
    print(f"Data saved to {filename}")


