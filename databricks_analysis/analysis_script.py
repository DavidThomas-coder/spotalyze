from pyspark.sql import SparkSession

def analyze_artist_trends(snowflake_table):
    """Analyze artist trends using data from Snowflake."""
    spark = SparkSession.builder.appName("Artist Trend Analysis").getOrCreate()
    
    # Read data from Snowflake into Spark
    df = spark.read.format("jdbc") \
       .option("url", snowflake_connection_string) \
       .option("dbtable", "top_songs_usa") \
       .load()
    
    result = spark.sql("""
    SELECT artist_name, COUNT(*) as plays_count
    FROM top_songs_usa
    GROUP BY artist_name
    ORDER BY plays_count DESC
    """)
    
    result.show()

