import random
import time
from flask import jsonify

class DHT22Simulator:
    def __init__(self):
        # Initialize with realistic starting values
        self.current_temp = 23.0  # Starting at 23°C
        self.current_humidity = 45.0  # Starting at 45%
        
        # Define realistic ranges
        self.temp_range = (10, 40)  # 10°C to 40°C
        self.humidity_range = (20, 80)  # 20% to 80%
        
        # Maximum change between readings
        self.max_temp_change = 0.5
        self.max_humidity_change = 2.0

    def _random_walk(self, current, max_change, min_val, max_val):
        """Generate next value using random walk within constraints"""
        change = random.uniform(-max_change, max_change)
        new_value = current + change
        
        # Keep within realistic bounds
        new_value = max(min_val, min(max_val, new_value))
        
        # Round to 1 decimal place like a real DHT22
        return round(new_value, 1)

    def get_sensor_data(self):
        """Generate next sensor reading"""
        # Update current values using random walk
        self.current_temp = self._random_walk(
            self.current_temp,
            self.max_temp_change,
            self.temp_range[0],
            self.temp_range[1]
        )
        
        self.current_humidity = self._random_walk(
            self.current_humidity,
            self.max_humidity_change,
            self.humidity_range[0],
            self.humidity_range[1]
        )
        
        # Return in the same format as your API would
        return {
            "temperature": self.current_temp,
            "humidity": self.current_humidity,
            "timestamp": int(time.time()),
            "sensor_id": "DHT22_SIM_001"
        }

# Create a singleton instance
sensor_simulator = DHT22Simulator()

def fetch_sensor_data():
    """
    Replacement for the API fetch function that uses simulated data instead.
    """
    try:
        data = sensor_simulator.get_sensor_data()
        return data
    except Exception as e:
        print(f"Error generating sensor data: {e}")
        return None