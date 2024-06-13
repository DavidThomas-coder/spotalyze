import pandas as pd
import snowflake.connector
import os
from dotenv import load_dotenv

load_dotenv()

def transform_data(raw_data):
    try:
        # Log raw_data for debugging
        print(f"raw_data: {raw_data}")

        # Assuming raw_data is a dictionary with 'items' as a list of song info
        if 'items' in raw_data:
            items = raw_data['items']
            # Extract relevant data
            songs = []
            for item in items:
                song_info = {
                    'id': item['id'],
                    'name': item['name'],
                    'artists': ", ".join([artist['name'] for artist in item['artists']]),
                    'album': item['album']['name'],
                    'popularity': item['popularity']
                }
                songs.append(song_info)
            
            # Convert list of song info to DataFrame
            df = pd.DataFrame(songs)
            return df
        else:
            print(f"Unexpected data format: {raw_data}")
            return None
    except Exception as e:
        print(f"Error transforming data: {e}")
        return None

def connect_to_snowflake():
    try:
        conn = snowflake.connector.connect(
            account=os.getenv('SNOWFLAKE_ACCOUNT'),
            user=os.getenv('SNOWFLAKE_USER'),
            password=os.getenv('SNOWFLAKE_PASSWORD'),
            warehouse=os.getenv('SNOWFLAKE_WAREHOUSE'),
            database=os.getenv('SNOWFLAKE_DATABASE'),
            schema=os.getenv('SNOWFLAKE_SCHEMA')
        )
        return conn
    except Exception as e:
        print(f"Error connecting to Snowflake: {e}")
        return None

def load_from_stage(conn, stage, table, format):
    try:
        cursor = conn.cursor()
        query = f"""
        COPY INTO {table}
        FROM @{stage}
        FILE_FORMAT = (FORMAT_NAME = '{format}')
        """
        cursor.execute(query)
        cursor.close()
        return True
    except Exception as e:
        print(f"Error loading data into Snowflake: {e}")
        return False



