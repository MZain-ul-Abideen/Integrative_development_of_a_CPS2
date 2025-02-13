import random
import time

class DHT22Simulator:
    def __init__(self):
        self.current_temp = 23.0
        self.current_humidity = 45.0
        self.temp_range = (10, 40)
        self.humidity_range = (20, 80)
        self.max_temp_change = 0.5
        self.max_humidity_change = 2.0

    def _random_walk(self, current, max_change, min_val, max_val):
        """
        Generate a new value using a random walk algorithm.
        """
        try:
            change = random.uniform(-max_change, max_change)
            new_val = current + change  # Define new_val here
            return round(max(min_val, min(new_val, max_val)), 1)  # Ensure new_val is within bounds
        except Exception as e:
            print(f"Error in random walk: {e}")
            return current  # Return the current value if there's an error

    def get_sensor_data(self):
        """
        Generate simulated sensor data.
        """
        try:
            self.current_temp = self._random_walk(self.current_temp, self.max_temp_change, *self.temp_range)
            self.current_humidity = self._random_walk(self.current_humidity, self.max_humidity_change, *self.humidity_range)

            return {
                "inside_temperature": self.current_temp,
                "inside_humidity": self.current_humidity,
                "sensor_id": "DHT22_SIM_001",
                "timestamp": int(time.time())
            }
        except Exception as e:
            print(f"Error fetching sensor data: {e}")
            return {}  # Return an empty dictionary if there's an error

# Singleton instance
sensor_simulator = DHT22Simulator()

def fetch_sensor_data():
    """
    Fetch simulated sensor data.
    """
    return sensor_simulator.get_sensor_data() or {}