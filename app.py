from flask import Flask
from spotify_api.api_handler import access_token, extract_top_songs
from snowflake_integration.snowflake_loader import transform_data, connect_to_snowflake, load_from_stage
from config import Config

app = Flask(__name__)

@app.route('/fetch_and_load', methods=['GET'])
def fetch_and_load():
    # Obtain Spotify access token
    access_token = access_token()

    # Fetch and transform data
    raw_data = extract_top_songs(access_token)
    transformed_data = transform_data(raw_data)

    # Connect to Snowflake using configuration from config.py
    snowflake_config = {
        'account': Config.SNOWFLAKE_ACCOUNT,
        'user': Config.SNOWFLAKE_USER,
        'password': Config.SNOWFLAKE_PASSWORD,
        'warehouse': Config.SNOWFLAKE_WAREHOUSE,
        'database': Config.SNOWFLAKE_DATABASE,
        'schema': Config.SNOWFLAKE_SCHEMA
    }
    conn = connect_to_snowflake(**snowflake_config)

    # Load data into Snowflake
    load_from_stage(conn, "my_stage", "top_songs_usa", "my_csv_format")

    return 'Data fetched and loaded into Snowflake.'

if __name__ == '__main__':
    app.run(debug=True)


