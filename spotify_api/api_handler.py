import requests
import os
from dotenv import load_dotenv
from flask import current_app
from.local_storage import save_data_locally

# Load environment variables from.env file
load_dotenv()

def access_token():
    """Obtain an access token from the Spotify API."""
    token_uri = "https://accounts.spotify.com/api/token"
    header = {'Content-Type': 'application/x-www-form-urlencoded'}
    token_request_body = {
        'grant_type': 'client_credentials',
        'client_id': os.getenv('SPOTIFY_CLIENT_ID'),  # Use environment variable
        'client_secret': os.getenv('SPOTIFY_CLIENT_SECRET')  # Use environment variable
    }
    response = requests.post(url=token_uri, headers=header, data=token_request_body)
    
    # Check if the request was successful
    if response.status_code == 200:
        token = response.json()['access_token']
        current_app.logger.debug(f"Obtained access token: {token[:10]}...")  # Log the first 10 characters for security
        return token
    else:
        current_app.logger.error(f"Failed to get access token: {response.text}")
        return None  # Return None on failure instead of raising an exception

def extract_top_songs(access_token):
    """Fetch top songs data from the Spotify API and save it locally."""
    url = "https://api.spotify.com/v1/playlists/37i9dQZEVXbLp5XoPON0wI/tracks?market=US"
    header = {'Authorization': f'Bearer {access_token}'}
    response = requests.get(url=url, headers=header)
    
    # Check if the request was successful
    if response.status_code == 200:
        data = response.json()
        save_data_locally([data], filename_prefix="spotify_top_songs")
        current_app.logger.debug(f"Fetched top songs data: {len(data['items'])} items")  # Log the number of items fetched
        return data
    else:
        current_app.logger.error(f"Failed to fetch top songs: {response.text}")
        return None  # Return None on failure instead of raising an exception
