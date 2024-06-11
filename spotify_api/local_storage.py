import json
import pandas as pd
from datetime import date

def save_data_locally(data, filename_prefix="spotify_top_songs"):
    """Save data to a local JSON file."""
    today = date.today()
    filename = f"{filename_prefix}_{today}.json"
    pd.concat(data).to_json(filename, orient='records')
    print(f"Data saved to {filename}")
