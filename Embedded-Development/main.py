# main.py -- put your code here!

# Import libraries
import utime
from machine import Pin, ADC
from dht import DHT22

# Pins
DHT_PIN = 21
LIGHT_SENSOR_PIN = 34
LED1_PIN = 13
LED2_PIN = 12
LED3_PIN = 27

# Initialize sensors and pins
dht_sensor = DHT22(Pin(DHT_PIN))
light_sensor = ADC(Pin(LIGHT_SENSOR_PIN))
light_sensor.atten(ADC.ATTN_11DB)  # Configure ADC to read 0-3.3V

led1 = Pin(LED1_PIN, Pin.OUT)
led2 = Pin(LED2_PIN, Pin.OUT)
led3 = Pin(LED3_PIN, Pin.OUT)

# Main loop
def main():
    while True:
        try:
            # Read DHT22 sensor values
            dht_sensor.measure()
            temperature = dht_sensor.temperature()
            humidity = dht_sensor.humidity()

            # Read light sensor value
            light_level = light_sensor.read()

            # Print sensor values to console
            print("Temperature:", temperature, "C")
            print("Humidity:", humidity, "%")
            print("Light Level:", light_level)

            # Example LED control logic (toggle LEDs for demonstration)
            led1.value(1)
            utime.sleep(0.5)
            led1.value(0)

            led2.value(1)
            utime.sleep(0.5)
            led2.value(0)

            led3.value(1)
            utime.sleep(0.5)
            led3.value(0)

            # Delay before next reading
            utime.sleep(5)
        except Exception as e:
            print("Error in main loop:", e)

if __name__ == "__main__":
    main()
