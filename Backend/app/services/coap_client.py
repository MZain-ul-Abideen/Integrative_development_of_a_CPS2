# /app/services/coap_client.py
import asyncio
import json
from aiocoap import *

async def fetch_dht_sensor_data(host):
    """
    Fetch DHT22 sensor data (temperature and humidity) from the ESP32 CoAP server.
    """
    try:
        protocol = await Context.create_client_context()
        request = Message(code=GET, uri=f'coap://{host}/sensors')

        response = await protocol.request(request).response
        data = json.loads(response.payload.decode('utf-8'))

        return data  # Return the sensor data as a dictionary

    except Exception as e:
        print(f"Error fetching sensor data from ESP32: {e}")
        return {}

async def update_led_states(host, payload):
    """
    Send a CoAP PUT request to control the LEDs on the ESP32.
    """
    try:
        protocol = await Context.create_client_context()
        request = Message(
            code=PUT,
            payload=json.dumps(payload).encode('utf-8'),
            uri=f'coap://{host}/leds'
        )

        response = await protocol.request(request).response
        data = json.loads(response.payload.decode('utf-8'))

        return data.get("status") == "success"

    except Exception as e:
        print(f"Error updating LED states via CoAP: {e}")
        return False