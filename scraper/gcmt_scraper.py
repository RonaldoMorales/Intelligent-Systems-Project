import requests
import sqlite3
from datetime import datetime

def get_usgs_data():
    base_url = "https://earthquake.usgs.gov/fdsnws/event/1/query"

    params = {
        "format": "geojson",
        "starttime": "2020-01-01",
        "endtime": "2020-12-31",
        "minlatitude": -60,
        "maxlatitude": 60,
        "minlongitude": -180,
        "maxlongitude": 180,
        "minmagnitude": 5.0
    }

    response = requests.get(base_url, params=params)
    data = response.json()
    return data["features"]

def save_to_sqlite(features):
    conn = sqlite3.connect("earthquakes.db")
    c = conn.cursor()

    # Create table if not exists
    c.execute("""
        CREATE TABLE IF NOT EXISTS earthquakes (
            id TEXT PRIMARY KEY,
            time TEXT,
            magnitude REAL,
            depth REAL,
            latitude REAL,
            longitude REAL,
            place TEXT
        )
    """)

    for feature in features:
        props = feature["properties"]
        geom = feature["geometry"]

        quake_id = feature["id"]
        time_utc = datetime.utcfromtimestamp(props["time"] / 1000).strftime('%Y-%m-%d %H:%M:%S')
        mag = props["mag"]
        place = props["place"]
        lon, lat, depth = geom["coordinates"]

        # Insert with conflict handling
        c.execute("""
            INSERT OR IGNORE INTO earthquakes (id, time, magnitude, depth, latitude, longitude, place)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (quake_id, time_utc, mag, depth, lat, lon, place))

    conn.commit()
    conn.close()
    print("✅ Data saved to earthquakes.db")

# Run both
features = get_usgs_data()
save_to_sqlite(features)
