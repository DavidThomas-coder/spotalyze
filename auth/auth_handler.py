import requests
from dotenv import load_dotenv
import os

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

