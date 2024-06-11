import requests
import json
from  config import SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET  # Import the credentials

def access_token():
    """Obtain an access token from the Spotify API."""
    token_uri = "https://accounts.spotify.com/api/token"
    header = {'Content-Type': 'application/x-www-form-urlencoded'}
    token_request_body = {
        'grant_type': 'client_credentials',
        'client_id': SPOTIFY_CLIENT_ID,  # Use imported value
        'client_secret': SPOTIFY_CLIENT_SECRET  # Use imported value
    }
    response = requests.post(url=token_uri, headers=header, data=token_request_body)
    return response.json()['access_token']

def extract_top_songs(access_token):
    """Fetch top songs data from the Spotify API."""
    url = "https://api.spotify.com/v1/playlists/37i9dQZEVXbLp5XoPON0wI/tracks?market=US"
    header = {'Authorization': f'Bearer {access_token}'}
    response = requests.get(url=url, headers=header)
    return response.json()