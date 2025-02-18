from machine import Pin
import network
import utime
import microcoapy
from coap_macros import COAP_METHOD
from dht import DHT22
import json
import uasyncio as asyncio

# Pin Definitions
class PinConfig:
    DHT_PIN = 21  # Pin for the DHT22 sensor
    LED1_PIN = 13  # Red
    LED2_PIN = 27  # Yellow
    LED3_PIN = 12  # Green

# LED Manager
class LEDManager:
    def __init__(self):
        # Initialize LEDs
        self.led1 = Pin(PinConfig.LED1_PIN, Pin.OUT)
        self.led2 = Pin(PinConfig.LED2_PIN, Pin.OUT)
        self.led3 = Pin(PinConfig.LED3_PIN, Pin.OUT)
        self.led_states = {
            "redLed": False,
            "yellowLed": False,
            "greenLed": False
        }

    def update_led_states(self, new_states):
        """Update LED states and physical LED outputs"""
        self.led_states.update(new_states)
        self.led1.value(self.led_states["redLed"])
        self.led2.value(self.led_states["yellowLed"])
        self.led3.value(self.led_states["greenLed"])

    def get_led_states(self):
        """Return current LED states"""
        return self.led_states

# Network Configuration
class NetworkConfig:
    WIFI_SSID = 'POCO X6 5G'  # Replace with your WiFi SSID
    WIFI_PASSWORD = 'amin1884'  # Replace with your WiFi password

# Sensor Management
class SensorManager:
    def __init__(self):
        # Initialize DHT22 sensor
        self.dht_sensor = DHT22(Pin(PinConfig.DHT_PIN))

    def get_sensor_data(self):
        """Get data from DHT22 sensor"""
        try:
            self.dht_sensor.measure()
            temperature = self.dht_sensor.temperature()
            humidity = self.dht_sensor.humidity()

            current_time = utime.localtime()
            timestamp = "{:04d}-{:02d}-{:02d} {:02d}:{:02d}:{:02d}".format(
                current_time[0], current_time[1], current_time[2],
                current_time[3], current_time[4], current_time[5]
            )

            return {
                "timestamp": timestamp,
                "temperature": temperature,
                "humidity": humidity
            }
        except Exception as e:
            print("Error reading DHT22 sensor:", str(e))
            return None

# Network Manager
class NetworkManager:
    @staticmethod
    async def connect_wifi():
        """Connect to WiFi network"""
        wlan = network.WLAN(network.STA_IF)
        wlan.active(True)
        
        if not wlan.isconnected():
            print('Connecting to network...')
            wlan.connect(NetworkConfig.WIFI_SSID, NetworkConfig.WIFI_PASSWORD)
            
            # Wait for connection with timeout
            start_time = utime.time()
            while not wlan.isconnected():
                if utime.time() - start_time > 20:  # 20 second timeout
                    raise Exception("WiFi connection timeout")
                await asyncio.sleep_ms(100)
                
        print('Network config:', wlan.ifconfig())
        return wlan

# CoAP Server
class SensorServer:
    def __init__(self, sensor_manager, led_manager):
        self.sensor_manager = sensor_manager
        self.led_manager = led_manager
        self.server = microcoapy.Coap()

    def setup(self):
        """Setup CoAP server and register endpoints"""
        def sensor_handler(packet, sender_ip, sender_port):
            print(f'Sensor endpoint accessed from: {sender_ip}:{sender_port}')
            
            if packet.method == COAP_METHOD.COAP_GET:
                sensor_data = self.sensor_manager.get_sensor_data()
                if sensor_data:
                    response = json.dumps(sensor_data)
                    self.server.sendResponse(
                        sender_ip,
                        sender_port,
                        packet.messageid,
                        response,
                        0x45,  # 2.05 Content
                        0,     # No specific content format
                        packet.token
                    )

        def led_handler(packet, sender_ip, sender_port):
            print(f'LED endpoint accessed from: {sender_ip}:{sender_port}')
            
            if packet.method in [COAP_METHOD.COAP_POST, COAP_METHOD.COAP_PUT]:
                try:
                    payload = json.loads(packet.payload.decode())
                    self.led_manager.update_led_states(payload)
                    response = json.dumps({"status": "success", "led_states": self.led_manager.get_led_states()})
                    self.server.sendResponse(
                        sender_ip,
                        sender_port,
                        packet.messageid,
                        response,
                        0x44,  # 2.04 Changed
                        0,     # No specific content format
                        packet.token
                    )
                except Exception as e:
                    print("Error processing LED request:", str(e))
                    self.server.sendResponse(
                        sender_ip,
                        sender_port,
                        packet.messageid,
                        json.dumps({"status": "error", "message": str(e)}),
                        0x50,  # 5.00 Internal Server Error
                        0,
                        packet.token
                    )

        self.server.addIncomingRequestCallback('sensors', sensor_handler)
        self.server.addIncomingRequestCallback('leds', led_handler)
        self.server.start()
        print('CoAP server started. Waiting for requests...')

    async def run(self):
        """Main server loop"""
        self.setup()
        while True:
            try:
                self.server.poll(1000)  # 1 second poll timeout
                await asyncio.sleep_ms(100)  # Allow other tasks to run
            except Exception as e:
                print("Server error:", str(e))
                await asyncio.sleep_ms(100)

# Main Application
class CoAPApplication:
    def __init__(self):
        self.sensor_manager = SensorManager()
        self.led_manager = LEDManager()
        self.sensor_server = SensorServer(self.sensor_manager, self.led_manager)

    async def run(self):
        """Run the main application"""
        try:
            # Connect to WiFi
            await NetworkManager.connect_wifi()
            
            # Create server task
            server_task = asyncio.create_task(self.sensor_server.run())
            
            # Wait for the server task
            await asyncio.gather(server_task)
            
        except Exception as e:
            print("Application error:", str(e))
        finally:
            # Cleanup if needed
            pass

# Entry point
if __name__ == '__main__':
    app = CoAPApplication()
    asyncio.run(app.run())