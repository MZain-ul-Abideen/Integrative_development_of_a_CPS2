from apscheduler.schedulers.background import BackgroundScheduler
from app.services.rule_engine import RuleEngine  # Use absolute import
from app.services.api_client import fetch_sensor_data, fetch_weather_data

# Create a scheduler instance
scheduler = BackgroundScheduler()

def execute_action(rule, data):
    """
    Execute the action specified by the rule
    """
    try:
        # Add your action execution logic here
        # Example:
        if rule.action == "send_notification":
            # Import notification service only when needed
            from .notification_service import send_notification
            message = f"Rule '{rule.name}' triggered. Temperature: {data.get('temperature')}°C, Humidity: {data.get('humidity')}%"
            send_notification(message)
        # Add more action types as needed
        
        print(f"Action executed successfully for rule: {rule.name}")
        return True
    except Exception as e:
        print(f"Error executing action for rule {rule.name}: {e}")
        return False

def start_timer_service(app):
    """
    Start the timer service to evaluate rules at fixed intervals.
    """
    @scheduler.scheduled_job('interval', seconds=60, id='rule_evaluation')
    def evaluate_rules_periodically():
        with app.app_context():
            try:
                # Record start time for performance monitoring
                start_time = datetime.now()

                # Fetch data from APIs
                sensor_data = fetch_sensor_data()
                if not sensor_data:
                    print("Failed to fetch sensor data")
                    return

                weather_data = fetch_weather_data()
                if not weather_data:
                    print("Failed to fetch weather data")
                    return

                # Combine data
                data = {**sensor_data, **weather_data}
                
                # Log the current data (for debugging)
                print(f"Current data: Temperature: {data.get('temperature')}°C, "
                      f"Humidity: {data.get('humidity')}%, "
                      f"Weather: {data.get('weather_condition', 'N/A')}")

                # Evaluate rules
                triggered_rules = RuleEngine.evaluate_rules(data)

                # Execute actions for triggered rules
                for rule in triggered_rules:
                    # Log rule trigger
                    print(f"Rule triggered: {rule.name} at {datetime.now()}")
                    print(f"Condition: {rule.condition}")
                    print(f"Current values: {data}")
                    
                    # Execute the rule's action
                    success = execute_action(rule, data)
                    
                    # Optional: Log rule execution to database
                    # log_rule_execution(rule, data, success)

                # Performance logging
                execution_time = (datetime.now() - start_time).total_seconds()
                print(f"Rule evaluation completed in {execution_time} seconds")
                print(f"Total rules triggered: {len(triggered_rules)}")

            except Exception as e:
                print(f"Error in rule evaluation cycle: {e}")

    try:
        # Start the scheduler
        scheduler.start()
        print("Timer service started successfully")
    except Exception as e:
        print(f"Error starting timer service: {e}")

def stop_timer_service():
    """
    Safely shut down the scheduler
    """
    try:
        scheduler.shutdown()
        print("Timer service stopped successfully")
    except Exception as e:
        print(f"Error stopping timer service: {e}")