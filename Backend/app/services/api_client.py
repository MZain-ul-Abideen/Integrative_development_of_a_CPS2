import requests
import os

def fetch_weather_data():
    """
    Fetch live weather data from the WeatherAPI.
    """
    try:
        api_key = os.getenv('WEATHERAPI_API_KEY')
        url = "https://api.weatherapi.com/v1/current.json"
        params = {
            "key": 'f1213da1b6bd48c2a0a162437250102',
            "q": "auto:ip",  # Use the user's current location based on IP
            "aqi": "no"      # Disable air quality index for simplicity
        }

        response = requests.get(url, params=params)
        response.raise_for_status()
        weather_response = response.json()

        current_weather = weather_response.get("current", {})
        condition = current_weather.get("condition", {}).get("text", "N/A")
        temperature = current_weather.get("temp_c", "N/A")
        humidity = current_weather.get("humidity", "N/A")

        return {
            "weather_condition": condition,  # Use consistent key name
            "outside_temperature": temperature,
            "outside_humidity": humidity
        }

    except requests.exceptions.RequestException as e:
        print(f"Error fetching weather data: {e}")
        return {}  # Return an empty dictionary if there's an error