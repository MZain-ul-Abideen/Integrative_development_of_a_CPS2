from flask import current_app
from flask_mail import Mail, Message
import os
import paho.mqtt.client as mqtt

class NotificationService:
    def __init__(self, app=None):
        if app:
            self.mail = Mail(app)
            self.setup_email_config(app)

    def setup_email_config(self, app):
        app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER', 'smtp.gmail.com')
        app.config['MAIL_PORT'] = int(os.getenv('MAIL_PORT', 587))
        app.config['MAIL_USE_TLS'] = os.getenv('MAIL_USE_TLS', 'true').lower() == 'true'
        app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
        app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
        app.config['MAIL_DEFAULT_SENDER'] = os.getenv('MAIL_DEFAULT_SENDER')

    @staticmethod
    def send_notification(data, notification_type='print', recipient=None):
        try:
            email_body = data.get("emailBody")
            subject = data.get("subject")

            if not email_body:
                print("Error: Email body is required for email notifications.")
                return False

            if not subject:
                print("Error: Subject is required for email notifications.")
                return False

            if notification_type == 'print':
                print(f"Sending notification: {email_body}")
                return True

            elif notification_type == 'email':
                if not recipient:
                    print("Error: Email recipient is required for email notifications.")
                    return False

                mail = Mail(current_app)

                msg = Message(
                    subject=subject,
                    recipients=[recipient],
                    body=email_body
                )

                mail.send(msg)
                print(f"Email sent to {recipient}: {email_body}")
                return True

            else:
                print(f"Unsupported notification type: {notification_type}")
                return False

        except KeyError as e:
            print(f"Missing key in data: {e}")
            return False

        except Exception as e:
            print(f"Error sending notification: {e}")
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
# Global instance
notification_service = NotificationService()