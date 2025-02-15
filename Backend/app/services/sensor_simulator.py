import random
import time
import asyncio
from .coap_client import fetch_dht_sensor_data

def fetch_sensor_data():
    """
    Fetch real sensor data from the ESP32 CoAP server.
    """
    try:
        # Replace '192.168.205.226' with the actual ESP32 IP address
        coap_data = asyncio.run(fetch_dht_sensor_data("192.168.123.226"))

        # Map CoAP data to the expected format
        return {
            "inside_temperature": coap_data.get("temperature", "N/A"),
            "inside_humidity": coap_data.get("humidity", "N/A"),
            "sensor_id": "DHT22_ESP32",
            "timestamp": int(time.time())
        }
    except Exception as e:
        print(f"Error fetching sensor data from ESP32: {e}")
        return {}