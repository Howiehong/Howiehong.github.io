import os
import sqlite3
from flask import Flask, jsonify, render_template, url_for, request

app = Flask(__name__)
app._static_folder = 'static'


def get_crashes():
    db_path = r'/Users/howard/Downloads/motor_vehicle_collisions/crashes.db'
    try:
        conn = sqlite3.connect(db_path)
        c = conn.cursor()
        c.execute("SELECT * FROM crashes LIMIT 1000;")
        rows = c.fetchall()
        return [dict(zip(['date', 'time', 'borough', 'zip_code', 'latitude', 'longitude'], row)) for row in rows]
    except Exception as e:
        print(f"Error retrieving crashes: {e}")
        return None

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/crashes")
def api_crashes():
    try:
        crashes = get_crashes()
        return jsonify(crashes)
    except Exception as e:
        print(f"Error retrieving crashes: {e}")
        return jsonify({"error": "Unable to retrieve crashes"})

@app.route('/filter')
def filter():
    year = request.args.get('year')
    month = request.args.get('month')
    print(f"Year: {year}")
    print(f"Month: {month}")

    # Construct your SQL query based on the year and month parameters
    if year:
        start_date = '01/01/' + year
        end_date = '12/31/' + year
        query = "SELECT * FROM crashes WHERE `CRASH_DATE` LIKE '{}' AND '{}' LIMIT 1000".format(start_date, end_date)
        if month:
            month_start = month + '/01' + '/' + year
            month_end = month + '/31' + '/' + year
            query = "SELECT * FROM crashes WHERE `CRASH_DATE` LIKE '{}' AND '{}' LIMIT 1000".format(month_start, month_end)
    elif month:
        query = "SELECT * FROM crashes WHERE `CRASH_DATE` LIKE '{}/%' LIMIT 1000".format(month)
    else:
        return jsonify({'error': 'Please provide a year or month parameter'})

    # Execute the query and return the results as a JSON response
    db_path = r'/Users/howard/Downloads/motor_vehicle_collisions/crashes.db'
    try:
        conn = sqlite3.connect(db_path)
        c = conn.cursor()
        results = c.execute(query).fetchall()  # fetch query results
        return jsonify(results)
    except Exception as e:
        print(f"Error retrieving crashes: {e}")
        return None

# Generate URLs for static files in your templates
@app.context_processor
def override_url_for():
    return dict(url_for=dated_url_for)

def dated_url_for(endpoint, **values):
    if endpoint == 'static':
        filename = values.get('filename', None)
        if filename:
            file_path = os.path.join(app.root_path, app.static_folder, filename)
            values['q'] = int(os.stat(file_path).st_mtime)
    return url_for(endpoint, **values)

if __name__ == "__main__":
    app.run(port=8000, debug=True)
