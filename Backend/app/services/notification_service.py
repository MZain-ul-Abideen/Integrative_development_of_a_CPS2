# /app/services/notification_service.py
from flask import current_app
from flask_mail import Mail, Message
import os
import requests
import paho.mqtt.client as mqtt
import asyncio
import json
from aiocoap import *

class NotificationService:
    def __init__(self):
        # Hardcoded SendGrid API key and default sender email
        self.sendgrid_api_key = "REDACTED_SENDGRID_KEY"  # Replace with your actual API key
        self.default_sender = "mohammadamin.norouzi.2023@gmail.com"  # Replace with your default sender email

    def send_notification(self, data, recipient=None):
        try:
            if not self.sendgrid_api_key:
                print("Error: SendGrid API key is not configured.")
                return False

            if not recipient:
                print("Error: No recipient specified for email.")
                return False

            email_body = data.get("emailBody")
            subject = data.get("subject")  # Keep 'subject' as it was before

            if not all([email_body, subject]):
                print("Error: Missing email body or subject.")
                return False

            print(f"Attempting to send email to {recipient}: {email_body}")  # Debug log

            # Construct the SendGrid API payload
            payload = {
                "personalizations": [
                    {
                        "to": [{"email": recipient}],
                        "subject": subject
                    }
                ],
                "from": {"email": self.default_sender},  # Use hardcoded default sender
                "content": [
                    {
                        "type": "text/plain",
                        "value": email_body
                    }
                ]
            }

            headers = {
                "Authorization": f"Bearer {self.sendgrid_api_key}",
                "Content-Type": "application/json"
            }

            # Send the email via SendGrid API
            response = requests.post(
                "https://api.sendgrid.com/v3/mail/send",
                json=payload,
                headers=headers
            )

            if response.status_code == 202:
                print(f"Email sent successfully to {recipient}: {email_body}")
                return True
            else:
                print(f"Failed to send email. Status code: {response.status_code}, Response: {response.text}")
                return False

        except KeyError as e:
            print(f"Missing key in email data: {e}")
            return False
        except Exception as e:
            print(f"Error sending email: {e}")
            return False
        
    @staticmethod
    def mqtt_publish(data):
        try:
            client = mqtt.Client()
            client.connect("193.49.165.40", 1883, 60)  # Connect to MQTT broker
            client.publish(data['topic'], data['payload'])  # Publish message
            client.disconnect()
            return True
        except Exception as e:
            print(f"Error publishing MQTT message: {e}")
            return False

    @staticmethod
    async def coap_update_leds(host, payload):
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

# Global instance
notification_service = NotificationService()
