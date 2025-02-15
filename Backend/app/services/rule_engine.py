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
        "every_day": 86400
    }

    @staticmethod
    def parse_condition(condition):
        """
        Parse the condition string into a tuple (variable, operator, value).
        """
        try:
            parts = condition.split()
            if len(parts) != 3:
                raise ValueError("Invalid condition format")
            
            variable = parts[0]
            op = parts[1]
            value = parts[2]

            # Handle timer-based conditions
            if variable == "timer":
                if value not in RuleEngine.TIMER_CONDITIONS:
                    raise ValueError(f"Unsupported timer interval: {value}")
                return variable, op, value

            # Handle numeric conditions
            if variable != "weather_condition":
                value = float(value)

            # Validate operator
            if op not in RuleEngine.OPERATORS:
                raise ValueError(f"Unsupported operator: {op}")

            return variable, op, value

        except Exception as e:
            print(f"Error parsing condition: {e}")
            return None

    @staticmethod
    def evaluate_condition(condition, data):
        """
        Evaluate a single rule's condition against the provided data.
        """
        parsed = RuleEngine.parse_condition(condition)
        if not parsed:
            return False

        variable, op, value = parsed

        # Handle timer-based conditions
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

        # Handle weather conditions
        if variable == "weather_condition":
            if variable not in data:
                print(f"Variable '{variable}' not found in sensor data.")
                return False

            return data[variable] == value  # Compare weather condition strings directly

        # Handle numeric conditions
        if variable not in data:
            print(f"Variable '{variable}' not found in sensor data.")
            return False

        try:
            sensor_value = float(data[variable])
            return RuleEngine.OPERATORS[op](sensor_value, float(value))
        except Exception as e:
            print(f"Error evaluating condition: {e}")
            return False

    @staticmethod
    def evaluate_rules(data):
        """
        Evaluate all active rules against the provided data.
        """
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
        """
        Periodically check and execute all triggered rules.
        """
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

                # Execute email actions
                if action.action_type == "Send Email":
                    email_address = action.parameters.get("emailAddress")
                    subject = action.parameters.get("subject")
                    email_body = action.parameters.get("emailBody")

                    if not email_body:
                        print(f"Email body is missing for rule: {rule.name}")
                        continue

                    try:
                        # Replace placeholders in the email body
                        email_body = email_body.format(**combined_data)

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

                    except KeyError as e:
                        print(f"Missing key in email body template: {e}")

                # Execute MQTT actions for building automation
                elif action.action_type == "Building Automation":
                    topic = action.parameters.get("topic")
                    payload = action.parameters.get("payload")

                    if not topic or not payload:
                        print(f"MQTT topic or payload is missing for rule: {rule.name}")
                        continue

                    try:
                        success = notification_service.mqtt_publish(
                            data={
                                "topic": topic,
                                "payload": payload
                            }
                        )

                        if success:
                            print(f"MQTT message sent successfully for rule: {rule.name}")
                        else:
                            print(f"Failed to send MQTT message for rule: {rule.name}")

                    except Exception as e:
                        print(f"Error sending MQTT message: {e}")

                # Execute LED toggle actions
                elif action.action_type == "Toggle LED":
                    led_state = action.parameters.get("ledState")

                    if led_state is None:
                        print(f"LED state is missing for rule: {rule.name}")
                        continue

                    try:
                        # Simulate LED toggle logic (or integrate with hardware)
                        print(f"LED toggled to {led_state} for rule: {rule.name}")

                    except Exception as e:
                        print(f"Error toggling LED: {e}")

                else:
                    print(f"Unsupported action type: {action.action_type}")

        return triggered_rules