from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    results = None  # Start with no results (for clean initial load)

    if request.method == 'POST':
        try:
            user_lat = float(request.form['latitude'])
            user_lon = float(request.form['longitude'])

            # Connect to database
            conn = sqlite3.connect('earthquakes.db')
            c = conn.cursor()
            c.execute("SELECT time, magnitude, depth, latitude, longitude, place FROM earthquakes")
            all_data = c.fetchall()
            conn.close()

            # Define the search tolerance in degrees (~5 degrees ≈ 500 km)
            tolerance = 5

            # Find earthquakes within the tolerance range
            results = []
            for row in all_data:
                time, mag, depth, lat, lon, place = row
                if abs(lat - user_lat) <= tolerance and abs(lon - user_lon) <= tolerance:
                    results.append({
                        'time': time,
                        'magnitude': mag,
                        'depth': depth,
                        'latitude': lat,
                        'longitude': lon,
                        'place': place,
                    })

        except ValueError:
            # If the input can't be converted to float, return an empty result
            results = []

    return render_template('index.html', results=results)

if __name__ == '__main__':
    app.run(debug=True)
