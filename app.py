from flask import Flask, jsonify
import logging
import pandas as pd
from spotify_api.api_handler import access_token, extract_top_tracks, transform_data

app = Flask(__name__)
app.logger.setLevel(logging.DEBUG)  # Set Flask's logger to DEBUG level

@app.route('/')
def index():
    return "Welcome to Spotalyze <a href='/fetch_and_analyze'>Click here to fetch and analyze Spotify data</a>"

@app.route('/fetch_and_analyze', methods=['GET'])
def fetch_and_analyze():
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

        # Optionally, you can return transformed_data as JSON for inspection
        return jsonify({
            "status": "success",
            "message": "Data fetched and transformed successfully.",
            "data": transformed_data.to_dict(orient='records')  # Convert DataFrame to JSON
        }), 200
    except Exception as e:
        app.logger.error(f"Unhandled exception in fetch_and_analyze: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)


