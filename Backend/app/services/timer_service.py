from apscheduler.schedulers.background import BackgroundScheduler
from app.services.rule_engine import RuleEngine
from flask import current_app

scheduler = BackgroundScheduler()

def start_timer_service(app):
    @scheduler.scheduled_job('interval', minutes=5, id='rule_evaluation')  # Evaluate every minute
    def evaluate_rules_periodically():
        with app.app_context():
            try:
                RuleEngine.check_and_execute_rules()
            except Exception as e:
                print(f"Error in rule evaluation cycle: {e}")

    scheduler.start()
    print("Timer service started successfully")

def stop_timer_service():
    try:
        scheduler.shutdown()
        print("Timer service stopped successfully")
    except Exception as e:
        print(f"Error stopping timer service: {e}")