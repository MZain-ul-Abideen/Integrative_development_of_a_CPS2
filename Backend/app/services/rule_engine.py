from app.models import Rule, db
from .sensor_simulator import fetch_sensor_data
from .api_client import fetch_weather_data
import operator
import time
from .notification_service import notification_service

class RuleEngine:
    OPERATORS = {
        '>': operator.gt,
        '<': operator.lt,
        '>=': operator.ge,
        '<=': operator.le,
        '==': operator.eq,
        '!=': operator.ne
    }

    TIMER_CONDITIONS = {
        "every_minute": 60,  # Interval in seconds
        "every_hour": 3600,
        "every_day": 86400
    }

    @staticmethod
    def parse_condition(condition):
        try:
            parts = condition.split()
            if len(parts) != 3:
                raise ValueError("Invalid condition format")
            variable = parts[0]
            op = parts[1]
            value = parts[2]

            if op not in RuleEngine.OPERATORS:
                if variable == "timer" and value in RuleEngine.TIMER_CONDITIONS:
                    return variable, op, value
                raise ValueError(f"Unsupported operator: {op}")

            if variable != "timer":
                value = float(value)

            return variable, op, value
        except Exception as e:
            print(f"Error parsing condition: {e}")
            return None

    @staticmethod
    def evaluate_condition(condition, data):
        parsed = RuleEngine.parse_condition(condition)
        if not parsed:
            return False
        variable, op, value = parsed

        if variable == "timer":
            last_executed = data.get("last_executed", 0)
            interval = RuleEngine.TIMER_CONDITIONS.get(value, None)
            if interval is None:
                print(f"Invalid timer interval: {value}")
                return False

            current_time = time.time()
            if current_time - last_executed >= interval:
                data["last_executed"] = current_time  # Update the last execution time
                return True
            return False

        if variable not in data:
            print(f"Variable '{variable}' not found in sensor data.")
            return False

        try:
            sensor_value = float(data[variable])
            return RuleEngine.OPERATORS[op](sensor_value, value)
        except Exception as e:
            print(f"Error evaluating condition: {e}")
            return False

    @staticmethod
    def evaluate_rules(data):
        active_rules = Rule.query.all()
        triggered_rules = []

        for rule in active_rules:
            try:
                if RuleEngine.evaluate_condition(rule.condition, data):
                    triggered_rules.append(rule)
            except Exception as e:
                print(f"Error evaluating rule {rule.id}: {e}")

        return triggered_rules

    @staticmethod
    def check_and_execute_rules():
        sensor_data = fetch_sensor_data() or {}
        weather_data = fetch_weather_data() or {}

        # Add a "last_executed" key for timer-based rules
        combined_data = {
            **sensor_data,
            **weather_data,
            "last_executed": sensor_data.get("last_executed", 0)  # Default to 0 if not set
        }

        triggered_rules = RuleEngine.evaluate_rules(combined_data)

        for rule in triggered_rules:
            print(f"Rule '{rule.name}' triggered. Executing linked actions...")
            for link in rule.trigger_action_links:
                action = link.action
                if action.action_type == "Send Email":
                    email_address = action.parameters.get("emailAddress")
                    subject = action.parameters.get("subject")
                    email_body = action.parameters.get("emailBody").format(**combined_data)

                    success = notification_service.send_notification(
                        data={
                            "emailBody": email_body,
                            "subject": subject
                        },
                        notification_type='email',
                        recipient=email_address
                    )

                    if success:
                        print(f"Email sent successfully for rule: {rule.name}")
                    else:
                        print(f"Failed to send email for rule: {rule.name}")

        return triggered_rules