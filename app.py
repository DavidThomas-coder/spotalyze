from flask import Flask, jsonify, redirect, url_for, request, session
from dotenv import load_dotenv
import logging
import requests
import pandas as pd
from spotify_api.api_handler import SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET, SPOTIFY_REDIRECT_URI
from snowflake_integration.snowflake_loader import transform_data, connect_to_snowflake, load_from_stage

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with a secure random key
app.logger.setLevel(logging.DEBUG)  # Set Flask's logger to DEBUG level

@app.route('/')
def index():
    return "Welcome to Spotalyze <a href='/login'>Click here to log in with Spotify</a>"

@app.route('/login')
def login():
    scope = 'user-top-read'
    auth_url = (
        'https://accounts.spotify.com/authorize'
        '?response_type=code'
        f'&client_id={SPOTIFY_CLIENT_ID}'
        f'&scope={scope}'
        f'&redirect_uri={SPOTIFY_REDIRECT_URI}'
    )
    return redirect(auth_url)

@app.route('/callback')
def callback():
    code = request.args.get('code')
    token_url = 'https://accounts.spotify.com/api/token'
    response = requests.post(token_url, data={
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': SPOTIFY_REDIRECT_URI,
        'client_id': SPOTIFY_CLIENT_ID,
        'client_secret': SPOTIFY_CLIENT_SECRET
    })

    response_data = response.json()
    access_token = response_data.get('access_token')
    refresh_token = response_data.get('refresh_token')

    if access_token:
        session['access_token'] = access_token
        session['refresh_token'] = refresh_token
        return redirect(url_for('fetch_and_load'))
    else:
        return "Error obtaining access token", 500

@app.route('/fetch_and_load')
def fetch_and_load():
    try:
        access_token = session.get('access_token')
        if not access_token:
            return redirect(url_for('login'))

        headers = {
            "Authorization": f"Bearer {access_token}"
        }
        response = requests.get('https://api.spotify.com/v1/me/top/tracks', headers=headers)
        data = response.json()

        if response.status_code == 401:
            app.logger.error("Access token is invalid or expired. Redirecting to login.")
            return redirect(url_for('login'))

        app.logger.debug(f"Raw data: {data}")

        transformed_data = transform_data(data)
        if not isinstance(transformed_data, pd.DataFrame):
            app.logger.error("Failed to transform data.")
            return jsonify({"status": "error", "message": "Failed to transform data."}), 500

        conn = connect_to_snowflake()
        if not conn:
            app.logger.error("Failed to connect to Snowflake.")
            return jsonify({"status": "error", "message": "Failed to connect to Snowflake."}), 500

        load_status = load_from_stage(conn, "my_stage", "top_songs_usa", "my_csv_format")
        if not load_status:
            app.logger.error("Failed to load data into Snowflake.")
            return jsonify({"status": "error", "message": "Failed to load data into Snowflake."}), 500

        return jsonify({"status": "success", "message": "Data fetched and loaded into Snowflake."}), 200
    except Exception as e:
        app.logger.error(f"Unhandled exception in fetch_and_load: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)


