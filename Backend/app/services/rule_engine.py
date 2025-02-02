from app.models import Rule, db
from .sensor_simulator import fetch_sensor_data
import operator

class RuleEngine:
    # Dictionary of allowed operators and their corresponding functions
    OPERATORS = {
        '>': operator.gt,
        '<': operator.lt,
        '>=': operator.ge,
        '<=': operator.le,
        '==': operator.eq,
        '!=': operator.ne
    }

    @staticmethod
    def parse_condition(condition):
        """
        Parse a condition string like "temperature > 30" into its components
        Returns (variable, operator, value) or None if invalid
        """
        try:
            # Split the condition into parts
            parts = condition.split()
            if len(parts) != 3:
                raise ValueError("Invalid condition format")

            variable = parts[0]
            op = parts[1]
            value = float(parts[2])  # Convert value to float

            if op not in RuleEngine.OPERATORS:
                raise ValueError(f"Unsupported operator: {op}")

            return variable, op, value
        except Exception as e:
            print(f"Error parsing condition: {e}")
            return None

    @staticmethod
    def evaluate_condition(condition, data):
        """
        Safely evaluate a single condition against provided data
        """
        parsed = RuleEngine.parse_condition(condition)
        if not parsed:
            return False

        variable, op, value = parsed
        
        if variable not in data:
            print(f"Variable {variable} not found in sensor data")
            return False

        try:
            sensor_value = float(data[variable])
            return RuleEngine.OPERATORS[op](sensor_value, value)
        except Exception as e:
            print(f"Error evaluating condition: {e}")
            return False

    @staticmethod
    def evaluate_rules(data):
        """
        Evaluate all active rules against the provided data.
        """
        active_rules = Rule.query.filter_by(is_active=True).all()
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
        Fetch sensor data and evaluate rules
        """
        sensor_data = fetch_sensor_data()
        if not sensor_data:
            print("Failed to fetch sensor data")
            return []

        triggered_rules = RuleEngine.evaluate_rules(sensor_data)
        
        # Log and execute actions for triggered rules
        for rule in triggered_rules:
            try:
                print(f"Rule '{rule.name}' triggered. Executing action: {rule.action}")
                # Here you can add action execution logic
                # For example:
                # execute_action(rule.action)
            except Exception as e:
                print(f"Error executing action for rule {rule.id}: {e}")

        return triggered_rules