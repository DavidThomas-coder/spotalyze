from flask import Flask, jsonify, redirect, url_for, request
from dotenv import load_dotenv
import logging
import pandas as pd  # Ensure pandas is imported for DataFrame checks
from spotify_api.api_handler import access_token, extract_top_songs
from snowflake_integration.snowflake_loader import transform_data, connect_to_snowflake, load_from_stage

# Load environment variables from.env file
load_dotenv()

app = Flask(__name__)
app.logger.setLevel(logging.DEBUG)  # Set Flask's logger to DEBUG level

@app.route('/')
def index():
    return "Welcome to Spotalyze <a href='/fetch_and_load'>Click here to fetch and load Spotify data</a>"

@app.route('/fetch_and_load', methods=['GET'])
def fetch_and_load():
    try:
        # Obtain Spotify access token
        access_token = access_token()
        if access_token:
            app.logger.debug(f"Obtained access token: {access_token[:10]}...")  # Log the first 10 characters for security
        else:
            app.logger.error("Failed to obtain Spotify access token.")
            return jsonify({"status": "error", "message": "Failed to obtain Spotify access token."}), 500

        raw_data = extract_top_songs(access_token)
        if raw_data:
            app.logger.debug(f"Raw data: {raw_data}")  # Inspect the raw data structure
        else:
            app.logger.error("Failed to fetch data from Spotify API.")
            return jsonify({"status": "error", "message": "Failed to fetch data from Spotify API."}), 500

        transformed_data = transform_data(raw_data)
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
