from flask import Flask, jsonify, request, render_template
import pandas as pd
from spotify_api.api_handler import access_token, extract_top_tracks, transform_data

app = Flask(__name__)

@app.route('/')
def index():
    return "Welcome to Spotalyze <a href='/fetch_and_load'>Click here to fetch and load Spotify data</a>"

@app.route('/fetch_and_load', methods=['GET'])
def fetch_and_load():
    try:
        access_token_value = access_token()
        if not access_token_value:
            return jsonify({"status": "error", "message": "Failed to obtain Spotify access token."}), 500

        raw_data = extract_top_tracks(access_token_value)
        if not raw_data:
            return jsonify({"status": "error", "message": "Failed to fetch data from Spotify API."}), 500

        transformed_data = transform_data(raw_data)
        if not isinstance(transformed_data, pd.DataFrame):
            return jsonify({"status": "error", "message": "Failed to transform data."}), 500

        # Perform analysis with Pandas here
        # Example: Calculate average popularity
        average_popularity = transformed_data['popularity'].mean()

        # Example: Group by artists and count top tracks
        top_artists = transformed_data.groupby('artists')['name'].count().nlargest(5)

        # Render template with data for display
        return render_template('analysis.html', average_popularity=average_popularity, top_artists=top_artists)

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)



