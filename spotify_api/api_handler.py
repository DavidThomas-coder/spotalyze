import requests
import json

def access_token(client_id, client_secret):
    """Obtain an access token from the Spotify API."""
    token_uri = "https://accounts.spotify.com/api/token"
    header = {'Content-Type': 'application/x-www-form-urlencoded'}
    token_request_body = {
        'grant_type': 'client_credentials',
        'client_id': client_id,
        'client_secret': client_secret
    }
    response = requests.post(url=token_uri, headers=header, data=token_request_body)
    return response.json()['access_token']

def extract_top_songs(access_token):
    """Fetch top songs data from the Spotify API."""
    url = "https://api.spotify.com/v1/playlists/37i9dQZEVXbLp5XoPON0wI/tracks?market=US"
    header = {'Authorization': f'Bearer {access_token}'}
    response = requests.get(url=url, headers=header)
    return response.json()


