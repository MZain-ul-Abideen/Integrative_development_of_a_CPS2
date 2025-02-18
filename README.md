Integrated Development of CPS2
## Table of Contents:
- Introduction
- Features
- Technologies Used
- Prerequisites
- Setup and Installation
- API Endpoints
- Usage Examples
- Database Schema
- CoAP Server on ESP32
- Build for Production
- Contributing
- License
- Contact

## Introduction

This project implements a rule-based automation system that integrates sensor data (e.g., temperature, humidity) and weather API data to trigger actions such as sending emails or controlling LEDs via CoAP. The system is modular, allowing users to define custom rules and link them with specific actions.

The backend is built using Flask, with SQLAlchemy for database management and SendGrid for email notifications. The frontend is built with Vue.js and interacts with the backend via RESTful API endpoints.

## Features

## Rule Management: Create, list, and delete rules based on conditions (e.g., inside_temperature < 20).

## Action Management:

Sending emails with dynamic placeholders.

Controlling LED states via CoAP.

Service Management: Manage services (e.g., Weather, IoT Devices).

Timer Service: Periodically evaluates rules and executes linked actions.

CoAP Integration: Communicates with an ESP32 device to control LEDs.

MQTT Integration: Optionally set comfort levels via MQTT.

Web Interface: Manage rules and actions via a Vue.js-based UI.

## Technologies Used
Backend: Flask, Flask-SQLAlchemy, Flask-Migrate, Flask-CORS, SendGrid SDK, aiocoap, paho-mqtt

Frontend: Vue.js (v3.2.13), Vue Router (v4.0.3), Axios (v1.7.9), NPM (v11.0.0)

Prerequisites
Before running the project, ensure you have the following installed:

- Backend:

``` Python 3.8+
pip install -r requirements.txt 
```
- Frontend:

```` Node.js (LTS recommended)
npm install  # or yarn install
````

- MicroPython (for ESP32):

```esptool.py --chip esp32 --port /dev/ttyUSB0 erase_flash
esptool.py --chip esp32 --port /dev/ttyUSB0 --baud 460800 write_flash -z 0x1000 firmware.bin
```

## Setup and Installation

- Backend Setup

1. Clone the repository:

``` git clone https://gitlab.emse.fr/scrum/Ecole-des-mines.git
cd /Ecole-des-mines
```
2. Install dependencies:

``` pip install -r requirements.txt ``` 

3. Configure environment variables (.env file):

``` MAIL_DEFAULT_SENDER=your-email@gmail.com
SENDGRID_API_KEY=your-sendgrid-api-key
WEATHERAPI_API_KEY=your-weather-api-key
DB_URL=sqlite:///app.db  # Use SQLite or another database
ESP32_HOST=192.168.123.226  # Replace with your ESP32's IP address
```
4. Initialize the database:

``` flask db init
flask db migrate -m "Initial migration"
flask db upgrade
```
5. Start the Flask app:

``` python run.py ```

The app will start on http://127.0.0.1:5000.

## Frontend Setup

1. Navigate to the frontend directory:

``` cd Frontend/ ```

2. Install dependencies:

``` npm install ```

3. Start the development server: 

``` npm run serve ```

Open your browser and visit http://localhost:8080 (default Vite port).

## API Endpoints

## Service Management

- Create a Service: POST /services
- List Services: GET /services

## Rule (Trigger) Management

- Create a Rule: POST /rules

``` 
{
  "service_id": 1,
  "name": "Low Inside Temp Alert",
  "condition": "inside_temperature < 20"
}
```
- List Rules: GET /rules

## Action Management

- Create an Action: POST /actions

```
{
  "service_id": 1,
  "name": "Send Low Temp Email",
  "action_type": "Send Email",
  "parameters": {
      "emailAddress": "amin.norozi77@gmail.com",
      "subject": "Low Temperature Alert: {inside_temperature}°C",
      "emailBody": "The current inside temperature is {inside_temperature}°C."
  }
}
```

- List Actions: GET /actions

## Linking Rules and Actions

- Link a Rule with an Action: POST /link-rule-action

```
{
  "rule_id": 1,
  "action_id": 1
}
```

- List Linked Rules and Actions: GET /linked-rules-actions

## Database Schema

1. Service: id, name
2. Rule: id, name, condition, service_id
3. Action: id, name, action_type, parameters, service_id
4. TriggerActionLink: id, rule_id, action_id

## CoAP Server on ESP32

## Retrieving Sensor Data

- CoAP GET Request:

``` coap get coap://<ESP32-IP>/sensors ```

- Response:

```
{
  "humidity": 54.7,
  "temperature": 12.2
}
```

## Controlling LEDs 

- CoAP PUT Request in Python:

``` 
import asyncio
from aiocoap import *

async def update_led(ip, payload):
    protocol = await Context.create_client_context()
    request = Message(code=PUT, uri=f"coap://{ip}/leds", payload=payload.encode('utf-8'))
    response = await protocol.request(request).response
    print(response.payload.decode('utf-8'))

payload = '{"redLed": true}'
asyncio.run(update_led("192.168.205.226", payload))
```

## Contributing

- Fork the repository.
- Create a new branch: git checkout -b feature/new-feature.
- Commit changes: git commit -m "Add new feature".
- Push to the branch: git push origin feature/new-feature.
- Submit a pull request.

## License

This project is licensed under the MIT License. See the LICENSE file for details.

## Contact

For questions or support, contact:  ``` mohammadamin.norouzi.2023@gmail.com ```





