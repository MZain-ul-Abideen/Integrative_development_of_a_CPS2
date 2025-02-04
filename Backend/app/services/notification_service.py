from app.models import NotificationTemplate, db
from flask_mail import Mail, Message
from flask import current_app, render_template  # To render HTML templates
import os

class NotificationService:
    def __init__(self, app=None):
        if app:
            self.mail = Mail(app)
            self.setup_email_config(app)

    def setup_email_config(self, app):
        """Configure email settings from environment or config"""
        app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER', 'smtp.gmail.com')
        app.config['MAIL_PORT'] = int(os.getenv('MAIL_PORT', 587))
        app.config['MAIL_USE_TLS'] = os.getenv('MAIL_USE_TLS', 'true').lower() == 'true'
        app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
        app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
        app.config['MAIL_DEFAULT_SENDER'] = os.getenv('MAIL_DEFAULT_SENDER')

    @staticmethod
    def send_notification(template_name, data, notification_type='print', recipient=None):
        """
        Send a notification using a template.

        :param template_name: Name of the notification template
        :param data: Dictionary of data to format the template
        :param notification_type: Type of notification (print, email, etc.)
        :param recipient: Email recipient (required for email notifications)
        """
        # Fetch the template
        template = NotificationTemplate.query.filter_by(name=template_name).first()

        if not template:
            print(f"Template '{template_name}' not found.")
            return False

        try:
            # Render the plain text message
            plain_text_content = template.template.format(**data)

            # Render the HTML content from the email template
            html_content = render_template("email.html", **data)

        except KeyError as e:
            print(f"Missing key in template data: {e}")
            return False

        # Send notification based on type
        if notification_type == 'print':
            print(f"Sending notification: {plain_text_content}")
            return True

        elif notification_type == 'email':
            if not recipient:
                print("Email recipient is required for email notifications")
                return False

            try:
                # Use current_app to access Flask app context
                mail = Mail(current_app)

                msg = Message(
                    subject=f"Notification: {template.name}",
                    recipients=[recipient],
                    body=plain_text_content,  # Plain text version
                    html=html_content         # HTML version
                )

                mail.send(msg)
                print(f"Email sent to {recipient}: {plain_text_content}")
                return True

            except Exception as e:
                print(f"Error sending email: {e}")
                return False

        else:
            print(f"Unsupported notification type: {notification_type}")
            return False

# Create a global instance
notification_service = NotificationService()