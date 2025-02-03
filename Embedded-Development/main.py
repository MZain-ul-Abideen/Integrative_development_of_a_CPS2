import network
import utime
import microcoapy
from coap_macros import COAP_METHOD
import uasyncio as asyncio

# Network Configuration
class NetworkConfig:
    WIFI_SSID = 'Galaxy A06 0a23'  # Replace with your WiFi SSID
    WIFI_PASSWORD = '12345678'  # Replace with your WiFi password

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
class HelloServer:
    def __init__(self):
        self.server = microcoapy.Coap()

    def setup(self):
        """Setup CoAP server and register endpoints"""
        def hello_handler(packet, sender_ip, sender_port):
            print(f'Request received from: {sender_ip}:{sender_port}')
            
            if packet.method == COAP_METHOD.COAP_GET:
                response = "Hello"
                self.server.sendResponse(
                    sender_ip,
                    sender_port,
                    packet.messageid,
                    response,
                    0x45,  # 2.05 Content
                    0,     # No specific content format
                    packet.token
                )

        self.server.addIncomingRequestCallback('hello', hello_handler)
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
        self.hello_server = HelloServer()

    async def run(self):
        """Run the main application"""
        try:
            # Connect to WiFi
            await NetworkManager.connect_wifi()
            
            # Create server task
            server_task = asyncio.create_task(self.hello_server.run())
            
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