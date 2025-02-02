import requests

def fetch_weather_data():
    """
    Fetch weather data from the WeatherAPI.
    Replace the URL with your actual WeatherAPI endpoint.
    """
    try:
        response = requests.get('https://api.weatherapi.com/v1/current.json', params={
            'key': 'f1213da1b6bd48c2a0a162437250102', 
            'q': 'auto:ip'  # Fetch weather for the current location
        })
        response.raise_for_status()  # Raise an error for bad status codes
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching weather data: {e}")
        return None