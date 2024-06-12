from flask import Flask, jsonify, redirect, url_for
from dotenv import load_dotenv
import os
from spotify_api.api_handler import access_token, extract_top_songs
from snowflake_integration.snowflake_loader import transform_data, connect_to_snowflake, load_from_stage

# Load environment variables from.env file
load_dotenv()

app = Flask(__name__)

@app.route('/')  # Add this route
def index():
    return "Welcome to Spotalyze!   <a href='/fetch_and_load'>Click here to fetch and load Spotify data</a>"

@app.route('/fetch_and_load', methods=['GET'])
def fetch_and_load():
    try:
        # Obtain Spotify access token
        access_token = access_token()
        
        # Check if access_token is None or empty
        if not access_token:
            return jsonify({"status": "error", "message": "Failed to obtain Spotify access token"}), 500

        # Fetch and transform data
        raw_data = extract_top_songs(access_token)
        if not raw_data:
            return jsonify({"status": "error", "message": "Failed to fetch data from Spotify API"}), 500

        transformed_data = transform_data(raw_data)

        # Connect to Snowflake using environment variables
        conn = connect_to_snowflake()
        if not conn:
            return jsonify({"status": "error", "message": "Failed to connect to Snowflake"}), 500

        # Load data into Snowflake
        load_status = load_from_stage(conn, "my_stage", "top_songs_usa", "my_csv_format")
        if not load_status:
            return jsonify({"status": "error", "message": "Failed to load data into Snowflake"}), 500

        return jsonify({"status": "success", "message": "Data fetched and loaded into Snowflake."}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)








