import asyncio
from aiocoap import Context, Message, Code

async def update_led(ip, payload):
    context = await Context.create_client_context()
    request = Message(code=Code.PUT, payload=payload.encode(), uri=f"coap://{ip}/leds")
    response = await context.request(request).response
    print(f"Response: {response.payload.decode()}")

# Example: Update the red LED
payload = '{"yellowLed": false, "redLed": true, "greenLed": true}'
asyncio.run(update_led("192.168.205.226", payload))  # Replace with your device's IP