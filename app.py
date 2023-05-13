import os
import sqlite3
import pymongo
from datetime import datetime
from flask import Flask, jsonify, render_template, url_for, request

app = Flask(__name__)
app._static_folder = 'static'


def get_crashes():
    try:
        # Connect to MongoDB
        client = pymongo.MongoClient("mongodb+srv://howardhong2000:test@nyccrash.kdyjvgn.mongodb.net/")
        db = client["NYC-Crashes"]
        collection = db["Crashes"]

        # Retrieve data from MongoDB
        cursor = collection.find().limit(1000)
        rows = [doc for doc in cursor]

        # Format the data as a list of dictionaries
        return [dict(zip(['date', 'time', 'borough', 'zip_code', 'latitude', 'longitude'], row.values())) for row in rows]
    except Exception as e:
        print(f"Error retrieving Crashes: {e}")
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

    # Construct your MongoDB query based on the year and month parameters
    if year:
        start_date = '01/01/' + year
        end_date = '12/31/' + year
        query = {'CRASH_DATE': {'$regex': '^\\d{2}/\\d{2}/' + year + '\\b.*\\b$'}}
        print(query)
        if month:
            query = {'CRASH_DATE': {'$regex': '^' + month + '/\\d{2}/' + year + '\\b.*\\b$'}}
            print(query)
    elif month:
        query = {'CRASH_DATE': {'$regex': '^' + month + '/\\d{2}/\\d{4}\\b.*\\b$'}}
        print(query)
    else:
        return jsonify({'error': 'Please provide a year or month parameter'})

    # Execute the query and return the results as a JSON response
    client = pymongo.MongoClient("mongodb+srv://howardhong2000:test@nyccrash.kdyjvgn.mongodb.net/")
    db = client["NYC-Crashes"]
    collection = db["Crashes"]
    results_raw = list(collection.find(query,{"_id": 0}).limit(1000))
    results = [list(result.values()) for result in results_raw]
    return jsonify(results)
    
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
