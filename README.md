# Weather API with Flask and Open-Meteo

This is a lightweight Flask API that fetches historical weather data using the [Open-Meteo API](https://open-meteo.com/). It provides two endpoints:

## Features

- `/weather/single`: Get weather data for a single location and date.
- `/weather/batch`: Upload a CSV file with multiple locations and dates.

## Setup

1. **Clone the repo**

```bash
git clone https://github.com/jerem1as/weather-api.git
cd weather-api
```

2. **Install dependencies using Poetry**

```bash
poetry install
```

3. **Run the app**

```bash
poetry run python weather_api/app.py
```

## Endpoints

### POST `/weather/single`

**Request Body (JSON):**
```json
{
  "latitude": 35.6895,
  "longitude": 139.6917,
  "date": "3/1/2024"
}
```

**Response:** Weather data from Open-Meteo.

---

### POST `/weather/batch`

**Form-Data:**
- `file`: CSV file with headers: `city,latitude,longitude,date`

**Example CSV Content:**
```
city,latitude,longitude,date
Tokyo,35.6895,139.6917,3/1/2024
```

**Response:** List of weather data per city.

## Notes
- Dates must be in `MM/DD/YYYY` format.
- Uses Open-Meteo's archive API.
- Docs available at `/docs`

## License
MIT
