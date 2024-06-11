import pandas as pd
import snowflake.connector

def transform_data(data):
    """Transform raw data into a workable Snowflake format."""
    items = data['items']
    tracks_info = [{'id': item['track']['id'], 'name': item['track']['name'], 'artist_name': item['track']['artists'][0]['name']} for item in items]
    df = pd.DataFrame(tracks_info)
    return df

def connect_to_snowflake(account, user, password, warehouse, database, schema):
    """Establish a connection to Snowflake."""
    conn = snowflake.connector.connect(
        user=user,
        password=password,
        account=account,
        warehouse=warehouse,
        database=database,
        schema=schema
    )
    return conn

def load_into_snowflake(df, conn):
    """Load transformed data into Snowflake."""
    cursor = conn.cursor()
    for index, row in df.iterrows():
        insert_query = f"""
        INSERT INTO top_songs_usa (id, name, artist_name)
        VALUES ('{row['id']', '{row['name']}', '{row['artist_name}');
        """
        cursor.execute(insert_query)
    conn.commit()

# Example usage
if __name__ == "__main__":
    # Example configuration - replace with your actual Snowflake credentials
    snowflake_config = {
        'account': '<your_snowflake_account>',
        'user': '<your_snowflake_user>',
        'password': '<your_snowflake_password>',
        'warehouse': '<your_snowflake_warehouse>',
        'database': '<your_snowflake_database>',
        'schema': '<your_snowflake_schema>'
    }

    # Connect to Snowflake
    conn = connect_to_snowflake(**snowflake_config)

    # Example data transformation and loading
    # Assume `data` is the raw data fetched from the Spotify API
    transformed_data = transform_data(data)
    load_into_snowflake(transformed_data, conn)

    # Close the connection
    conn.close()


