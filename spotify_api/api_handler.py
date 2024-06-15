import os
import requests
from dotenv import load_dotenv

load_dotenv()

SPOTIFY_CLIENT_ID = os.getenv('SPOTIFY_CLIENT_ID')
SPOTIFY_CLIENT_SECRET = os.getenv('SPOTIFY_CLIENT_SECRET')

def access_token():
    try:
        # Spotify API token URL
        auth_url = "https://accounts.spotify.com/api/token"
        
        # Basic authentication for the request
        auth_response = requests.post(auth_url, {
            'grant_type': 'client_credentials',
            'client_id': SPOTIFY_CLIENT_ID,
            'client_secret': SPOTIFY_CLIENT_SECRET,
        })
        
        # Convert the response to JSON
        auth_response_data = auth_response.json()
        
        # Extract the access token
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
        # Example endpoint to get top tracks (global)
        url = "https://api.spotify.com/v1/playlists/37i9dQZEVXbMDoHDwVN2tF/tracks"  # Spotify's Top 50 Global playlist
        headers = {
            "Authorization": f"Bearer {access_token}"
        }
        
        response = requests.get(url, headers=headers)
        data = response.json()

        # Log the raw data to inspect its structure
        print(f"Raw data: {data}")

        return data
    except Exception as e:
        print(f"Error fetching top tracks: {e}")
        return None



