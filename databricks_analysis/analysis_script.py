from pyspark.sql import SparkSession

spark = SparkSession.builder.appName("Artist Trend Analysis").getOrCreate()

# Assuming you have a DataFrame `df` loaded from Snowflake
df.createOrReplaceTempView("top_songs")

# Count occurrences of each artist
result = spark.sql("""
SELECT artist_name, COUNT(*) as plays_count
FROM top_songs
GROUP BY artist_name
ORDER BY plays_count DESC
""")

result.show()
