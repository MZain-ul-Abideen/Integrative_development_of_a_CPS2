import requests
import os
from datetime import datetime
from typing import Optional, Dict, Any, Tuple
from requests.auth import HTTPBasicAuth

class MeteomaticsClient:
    """Client for interacting with the Meteomatics Weather API"""
    
    BASE_URL = "https://api.meteomatics.com"
    
    # Default coordinates (Saint-Etienne)
    DEFAULT_LAT = 45.4397
    DEFAULT_LON = 4.3872
    
    def __init__(self):
        """Initialize the client with credentials"""
        self.username = os.getenv("METEOMATICS_USERNAME")
        self.password = os.getenv("METEOMATICS_PASSWORD")
        
        if not self.username or not self.password:
            raise ValueError("METEOMATICS_USERNAME and METEOMATICS_PASSWORD must be set in environment variables")
    
    def parse_location(self, location: Optional[str] = None) -> str:
        """
        Parse location string or return default coordinates
        
        Args:
            location (str, optional): Location string in format "lat,lon" or None
        
        Returns:
            str: Formatted location string for API
        """
        if not location:
            return f"{self.DEFAULT_LAT},{self.DEFAULT_LON}"
            
        try:
            if "," in location:
                lat, lon = map(float, location.split(","))
                return f"{lat},{lon}"
            else:
                # If it's not coordinates, return default
                return f"{self.DEFAULT_LAT},{self.DEFAULT_LON}"
        except ValueError:
            # If parsing fails, return default
            return f"{self.DEFAULT_LAT},{self.DEFAULT_LON}"
    
    def get_weather_data(self, location: Optional[str] = None, 
                        parameters: Optional[list[str]] = None) -> Optional[Dict[str, Any]]:
        """
        Get weather data for a location
        
        Args:
            location (str, optional): Location in format "latitude,longitude" or city name
            parameters (list, optional): List of weather parameters to fetch
        """
        try:
            # Use default parameters if none provided
            if parameters is None:
                parameters = [
                    "t_2m:C",                  # Temperature at 2m in Celsius
                    "precip_1h:mm",            # Precipitation in last hour
                    "wind_speed_10m:ms",       # Wind speed at 10m
                    "relative_humidity_2m:p",   # Relative humidity
                    "weather_symbol_1h:idx"     # Weather symbol
                ]
            
            # Format current time
            now = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
            
            # Parse location
            parsed_location = self.parse_location(location)
            
            # Join parameters with comma
            params_str = ",".join(parameters)
            
            # Format URL
            url = f"{self.BASE_URL}/{now}/{params_str}/{parsed_location}/json"
            
            response = requests.get(
                url,
                auth=HTTPBasicAuth(self.username, self.password),
                timeout=10
            )
            
            # Print debug info
            print(f"Request URL: {url}")
            print(f"Status Code: {response.status_code}")
            
            response.raise_for_status()
            return response.json()
            
        except requests.exceptions.RequestException as e:
            print(f"Error fetching weather data: {e}")
            return None

def get_weather_forecast(location: Optional[str] = None) -> Optional[Dict[str, Any]]:
    """
    Get weather forecast for a location
    
    Args:
        location (str, optional): Location identifier. If None, uses default coordinates
    """
    try:
        client = MeteomaticsClient()
        return client.get_weather_data(location)
        
    except Exception as e:
        print(f"Error in weather service: {e}")
        return None

# Example usage
if __name__ == "__main__":
    # Test with default location
    weather_default = get_weather_forecast()
    print("Weather for default location:", weather_default)
    
    # Test with specific location
    weather_specific = get_weather_forecast("51.5074,-0.1278")  # London
    print("Weather for London:", weather_specific)