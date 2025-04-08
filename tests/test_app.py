import pytest
from weather_api.app import app

@pytest.fixture
def client():
    app.testing = True
    with app.test_client() as client:
        yield client

def test_weather_single_ok(client):
    payload = {
        "latitude": 35.6895,
        "longitude": 139.6917,
        "date": "3/1/2024"
    }
    response = client.post("/weather/single", json=payload)
    assert response.status_code == 200
    json_data = response.get_json()
    assert "daily" in json_data
    assert "time" in json_data["daily"]