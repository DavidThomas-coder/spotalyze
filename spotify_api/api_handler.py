import os
import requests
from dotenv import load_dotenv
from flask import redirect, request

load_dotenv()

SPOTIFY_CLIENT_ID = os.getenv('SPOTIFY_CLIENT_ID')
SPOTIFY_CLIENT_SECRET = os.getenv('SPOTIFY_CLIENT_SECRET')
SPOTIFY_REDIRECT_URI = "http://localhost:5000/callback"

def get_auth_url():
    auth_url = "https://accounts.spotify.com/authorize"
    response_type = "code"
    scope = "user-top-read"
    redirect_uri = SPOTIFY_REDIRECT_URI

    auth_query = f"{auth_url}?response_type={response_type}&client_id={SPOTIFY_CLIENT_ID}&scope={scope}&redirect_uri={redirect_uri}"
    return auth_query

def get_token(auth_code):
    token_url = "https://accounts.spotify.com/api/token"
    payload = {
        'grant_type': 'authorization_code',
        'code': auth_code,
        'redirect_uri': SPOTIFY_REDIRECT_URI,
        'client_id': SPOTIFY_CLIENT_ID,
        'client_secret': SPOTIFY_CLIENT_SECRET
    }
    response = requests.post(token_url, data=payload)
    response_data = response.json()

    if response.status_code != 200:
        print(f"Error obtaining access token: {response_data}")
        return None

    return response_data['access_token']

def extract_top_songs(access_token):
    try:
        url = "https://api.spotify.com/v1/me/top/tracks"
        headers = {
            "Authorization": f"Bearer {access_token}"
        }
        response = requests.get(url, headers=headers)
        data = response.json()

        print(f"Raw data: {data}")

        return data
    except Exception as e:
        print(f"Error fetching top songs: {e}")
        return None
