import requests
import json
from datetime import date

from auth import get_access_token

def extract_spotify_data(client_id, client_secret):
    access_token = get_access_token(client_id, client_secret)
    url = "https://api.spotify.com/v1/playlists/<playlist_id>/tracks"  # Replace <playlist_id> with your target playlist ID
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(url=url, headers=headers)
    return response.json()

