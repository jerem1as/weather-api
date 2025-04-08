from flask import Flask, request, jsonify
from flask_restx import Api, Resource, fields
import requests
import csv
import io
from datetime import datetime

app = Flask(__name__)
api = Api(app, version='1.0', title='Weather API', description='API to fetch historical weather data using Open-Meteo', doc='/docs')

ns = api.namespace('weather', description='Weather operations')

OPEN_METEO_URL = "https://archive-api.open-meteo.com/v1/archive"

weather_input = api.model('WeatherInput', {
    'latitude': fields.Float(required=True),
    'longitude': fields.Float(required=True),
    'date': fields.String(required=True, example='3/1/2024')
})


def fetch_weather(lat, lon, date):
    """
    Fetches historical weather data from Open-Meteo API for a given location and date.

    Args:
        lat (float): Latitude of the location.
        lon (float): Longitude of the location.
        date (str): Date in 'MM/DD/YYYY' format.

    Returns:
        dict: A dictionary containing weather data if successful, or an error message.
    """
    try:
        formatted_date = datetime.strptime(date, "%m/%d/%Y").date()
        params = {
            "latitude": lat,
            "longitude": lon,
            "start_date": formatted_date,
            "end_date": formatted_date,
            "daily": "temperature_2m_max,temperature_2m_min,precipitation_sum",
            "timezone": "auto"
        }
        response = requests.get(OPEN_METEO_URL, params=params)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        return {"error": str(e)}


@ns.route('/single')
class WeatherSingle(Resource):
    """Handles POST requests to retrieve weather data for a single location."""
    @ns.expect(weather_input)
    def post(self):
        data = request.get_json()
        lat = data.get("latitude")
        lon = data.get("longitude")
        date = data.get("date")
        if not all([lat, lon, date]):
            return {"error": "Missing latitude, longitude or date"}, 400
        weather = fetch_weather(lat, lon, date)
        return weather


@ns.route('/batch')
class WeatherBatch(Resource):
    """Handles batch weather data requests from a CSV file."""
    def post(self):
        if 'file' not in request.files:
            return {"error": "No file part"}, 400

        file = request.files['file']
        if file.filename == '':
            return {"error": "No selected file"}, 400

        results = []
        stream = io.StringIO(file.stream.read().decode("UTF8"), newline=None)
        reader = csv.DictReader(stream)

        for row in reader:
            city = row.get("city")
            lat = row.get("latitude")
            lon = row.get("longitude")
            date = row.get("date")
            weather = fetch_weather(lat, lon, date)
            results.append({"city": city, "data": weather})

        return results


if __name__ == "__main__":
    app.run(debug=True)
