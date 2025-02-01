from app.models import Rule, db

class RuleEngine:
    @staticmethod
    def evaluate_rules(data):
        """
        Evaluate all active rules against the provided data.
        """
        active_rules = Rule.query.filter_by(is_active=True).all()
        triggered_rules = []

        for rule in active_rules:
            try:
                # Evaluate the condition (e.g., "temperature > 30")
                if eval(rule.condition, {}, data):
                    triggered_rules.append(rule)
            except Exception as e:
                print(f"Error evaluating rule {rule.id}: {e}")

        return triggered_rules