import pandas as pd
import snowflake.connector
import os
from dotenv import load_dotenv

# Load environment variables from.env file
load_dotenv()

def transform_data(data):
    """Transform raw data into a workable Snowflake format."""
    items = data['items']
    tracks_info = [{'id': item['track']['id'], 'name': item['track']['name'], 'artist_name': item['track']['artists'][0]['name']} for item in items]
    df = pd.DataFrame(tracks_info)
    return df

def connect_to_snowflake():
    """Establish a connection to Snowflake using environment variables."""
    conn = snowflake.connector.connect(
        user=os.getenv('SNOWFLAKE_USER'),
        password=os.getenv('SNOWFLAKE_PASSWORD'),
        account=os.getenv('SNOWFLAKE_ACCOUNT'),
        warehouse=os.getenv('SNOWFLAKE_WAREHOUSE'),
        database=os.getenv('SNOWFLAKE_DATABASE'),
        schema=os.getenv('SNOWFLAKE_SCHEMA')
    )
    return conn

def load_into_snowflake(df, conn):
    """Load transformed data into Snowflake."""
    cursor = conn.cursor()
    for index, row in df.iterrows():
        insert_query = f"""
        INSERT INTO top_songs_usa (id, name, artist_name)
        VALUES ('{row['id']}', '{row['name']}', '{row['artist_name']}');
        """
        cursor.execute(insert_query)
    conn.commit()


def save_df_to_csv(df, filename="spotify_data.csv"):
    """Save DataFrame to a CSV file."""
    df.to_csv(filename, index=False)

def load_from_stage(conn, stage_name, table_name, file_format_name):
    """Load data from a stage into a Snowflake table."""
    cursor = conn.cursor()
    copy_query = f"""
    COPY INTO {table_name}
    FROM @{stage_name}
    FILE_FORMAT = (TYPE = 'CSV' FORMAT_NAME = '{file_format_name}')
    """
    cursor.execute(copy_query)
    conn.commit()

# Example usage
if __name__ == "__main__":
    # Connect to Snowflake using environment variables
    conn = connect_to_snowflake()

    # Example data transformation and loading
    # Assume `data` is the raw data fetched from the Spotify API
    transformed_data = transform_data(data)
    save_df_to_csv(transformed_data, "spotify_data.csv")  # Save to CSV

    # Upload the CSV to a Snowflake stage (manual step or automated via `snowsql`)
    load_from_stage(conn, "my_stage", "top_songs_usa", "my_csv_format")  # Replace with your actual stage and format names

    # Close the connection
    conn.close()
