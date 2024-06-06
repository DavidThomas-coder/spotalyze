-- Example SQL to load JSON data into Snowflake
CREATE OR REPLACE TABLE top_songs_usa (
    id STRING,
    name STRING,
    artist_name STRING
);

COPY INTO top_songs_usa
FROM '@path_to_your_json_file'
FILE_FORMAT = (TYPE = 'JSON');
