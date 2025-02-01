from app.models import NotificationTemplate, db

class NotificationService:
    @staticmethod
    def send_notification(template_name, data):
        """
        Send a notification using a template.
        """
        template = NotificationTemplate.query.filter_by(name=template_name).first()
        if template:
            message = template.template.format(**data)
            print(f"Sending notification: {message}")
            # Add email or other notification logic here
        else:
            print(f"Template '{template_name}' not found.")