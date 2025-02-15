from app.models import Rule, TriggerActionLink, db
from .sensor_simulator import fetch_sensor_data
from .api_client import fetch_weather_data
from .notification_service import notification_service
import operator
import time

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
        "every_2_hours": 7200,
        "every_3_hours": 10800,
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

            if variable == "timer":
                if value not in RuleEngine.TIMER_CONDITIONS:
                    raise ValueError(f"Unsupported timer interval: {value}")
                return variable, op, value

            if op not in RuleEngine.OPERATORS:
                raise ValueError(f"Unsupported operator: {op}")

            if variable in ["inside_temperature", "outside_temperature"]:
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
            if variable == "weather_condition":
                return data[variable] == value  # Compare weather condition strings directly

            sensor_value = float(data[variable])
            return RuleEngine.OPERATORS[op](sensor_value, float(value))

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

                if action.action_type == "Building Automation":
                    comfort_level = action.parameters.get("comfort_level")
                    if comfort_level:
                        success = notification_service.mqtt_publish(
                            data={
                                "topic": "emse/fayol/2ET/220/temperature/setpoint",
                                "payload": str(comfort_level)
                            }
                        )
                        if success:
                            print(f"MQTT message sent for rule: {rule.name}")
                        else:
                            print(f"Failed to send MQTT message for rule: {rule.name}")

                elif action.action_type == "Send Email":
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

                elif action.action_type == "Toggle LED":
                    red_led = action.parameters.get("red_led", False)
                    green_led = action.parameters.get("green_led", False)
                    blue_led = action.parameters.get("blue_led", False)

                    if red_led or green_led or blue_led:
                        print(f"LED toggled for rule: {rule.name}")
                        # Simulate LED toggle logic (or integrate with hardware)
                        if red_led:
                            print("Red LED turned ON")
                        if green_led:
                            print("Green LED turned ON")
                        if blue_led:
                            print("Blue LED turned ON")

                else:
                    print(f"Unsupported action type: {action.action_type}")

        return triggered_rules