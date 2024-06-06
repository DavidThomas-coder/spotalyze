import pandas as pd

def transform_data(data):
    """Transform raw data into a structured format suitable for Snowflake."""
    df = pd.DataFrame(data['items'])
    df['id'] = df['track']['id']
    df['name'] = df['track']['name']
    df['artist_name'] = df['track']['artists'][0]['name']
    return df

def load_into_snowflake(df, snowflake_connection_string):
    """Load transformed data into Snowflake."""
    # Assuming you have a function to execute SQL commands through Snowflake
    execute_sql_command(f"INSERT INTO top_songs_usa (id, name, artist_name) VALUES {df.to_sql()}")

