from flask import Flask, jsonify, request
from dotenv import load_dotenv
import logging
import pandas as pd
from spotify_api.api_handler import access_token, extract_top_tracks, transform_data
from snowflake_integration.snowflake_loader import connect_to_snowflake, load_from_stage

load_dotenv()

app = Flask(__name__)
app.logger.setLevel(logging.DEBUG)  # Set Flask's logger to DEBUG level

@app.route('/')
def index():
    return "Welcome to Spotalyze <a href='/fetch_and_load'>Click here to fetch and load Spotify data</a>"

@app.route('/fetch_and_load', methods=['GET'])
def fetch_and_load():
    try:
        app.logger.debug("Attempting to obtain Spotify access token...")
        access_token_value = access_token()
        if access_token_value:
            app.logger.debug(f"Obtained access token: {access_token_value[:10]}...")  # Log the first 10 characters for security
        else:
            app.logger.error("Failed to obtain Spotify access token.")
            return jsonify({"status": "error", "message": "Failed to obtain Spotify access token."}), 500

        raw_data = extract_top_tracks(access_token_value)
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

