from apscheduler.schedulers.background import BackgroundScheduler
from .rule_engine import RuleEngine
from .api_client import fetch_sensor_data, fetch_weather_data

# Create a scheduler instance
scheduler = BackgroundScheduler()

def start_timer_service(app):
    """
    Start the timer service to evaluate rules at fixed intervals.
    """
    @scheduler.scheduled_job('interval', seconds=60, id='rule_evaluation')
    def evaluate_rules_periodically():
        with app.app_context():
            # Fetch data from APIs
            sensor_data = fetch_sensor_data()
            weather_data = fetch_weather_data()

            # Combine data
            data = {**sensor_data, **weather_data}

            # Evaluate rules
            triggered_rules = RuleEngine.evaluate_rules(data)

            # Perform actions for triggered rules
            for rule in triggered_rules:
                print(f"Rule triggered: {rule.name}")

    # Start the scheduler
    scheduler.start()