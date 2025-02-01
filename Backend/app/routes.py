from flask import Blueprint, jsonify, request
from http import HTTPStatus
from typing import Dict, Any, List
from .models import db, Rule
from .services.weather_service import get_weather_forecast
from .services.sensor_service import get_sensor_data
from .services.building_service import control_building
from .services.notification_service import send_notification

main = Blueprint('main', __name__)

def validate_rule_data(data: Dict[str, Any]) -> tuple[bool, str]:
    """Validate incoming rule data"""
    required_fields = ['name', 'trigger_service', 'trigger_condition', 
                      'action_service', 'action_details']
    
    for field in required_fields:
        if field not in data:
            return False, f"Missing required field: {field}"
            
    # Validate trigger service
    valid_trigger_services = ['weather', 'sensor']
    if data['trigger_service'] not in valid_trigger_services:
        return False, f"Invalid trigger service. Must be one of: {valid_trigger_services}"
    
    # Validate action service
    valid_action_services = ['notification', 'building']
    if data['action_service'] not in valid_action_services:
        return False, f"Invalid action service. Must be one of: {valid_action_services}"
    
    return True, ""

@main.route('/weather', methods=['GET'])
def get_default_weather():
    weather_data = get_weather_forecast()  # This will use default coordinates
    if weather_data:
        return jsonify(weather_data), 200
    return jsonify({"error": "Failed to fetch weather data"}), 500

@main.route('/weather/<location>', methods=['GET'])
def get_weather(location):
    weather_data = get_weather_forecast(location)
    if weather_data:
        return jsonify(weather_data), 200
    return jsonify({"error": "Failed to fetch weather data"}), 500

@main.route('/rules', methods=['GET', 'POST'])
def manage_rules():
    """Endpoint to manage automation rules"""
    try:
        if request.method == 'POST':
            data = request.json
            
            # Validate input data
            is_valid, error_message = validate_rule_data(data)
            if not is_valid:
                return jsonify({
                    "error": error_message
                }), HTTPStatus.BAD_REQUEST
            
            # Create new rule
            new_rule = Rule(
                name=data['name'],
                trigger_service=data['trigger_service'],
                trigger_condition=data['trigger_condition'],
                action_service=data['action_service'],
                action_details=data['action_details']
            )
            
            db.session.add(new_rule)
            db.session.commit()
            
            return jsonify({
                "message": "Rule created successfully",
                "rule_id": new_rule.id
            }), HTTPStatus.CREATED
            
        # GET request - fetch all rules
        rules = Rule.query.all()
        return jsonify({
            "status": "success",
            "data": [{
                "id": rule.id,
                "name": rule.name,
                "trigger_service": rule.trigger_service,
                "trigger_condition": rule.trigger_condition,
                "action_service": rule.action_service,
                "action_details": rule.action_details
            } for rule in rules]
        }), HTTPStatus.OK
        
    except Exception as e:
        return jsonify({
            "error": str(e)
        }), HTTPStatus.INTERNAL_SERVER_ERROR

@main.route('/evaluate-rules', methods=['GET'])
def evaluate_rules():
    """Endpoint to evaluate and execute automation rules"""
    try:
        rules = Rule.query.all()
        results: List[Dict[str, Any]] = []
        
        for rule in rules:
            try:
                if rule.trigger_service == "weather":
                    weather_data = get_weather_forecast("12345")  # Consider making location configurable
                    
                    # Safely evaluate the condition
                    if weather_data and eval(
                        rule.trigger_condition, 
                        {"weather": weather_data, "__builtins__": {}}  # Restrict eval context
                    ):
                        # Execute actions based on the rule
                        if rule.action_service == "notification":
                            send_notification(rule.action_details)
                        elif rule.action_service == "building":
                            control_building(rule.action_details, "on")
                            
                        results.append({
                            "rule_id": rule.id,
                            "status": "executed",
                            "name": rule.name
                        })
                    else:
                        results.append({
                            "rule_id": rule.id,
                            "status": "not_triggered",
                            "name": rule.name
                        })
                        
            except Exception as rule_error:
                results.append({
                    "rule_id": rule.id,
                    "status": "error",
                    "name": rule.name,
                    "error": str(rule_error)
                })
                
        return jsonify({
            "status": "success",
            "results": results
        }), HTTPStatus.OK
        
    except Exception as e:
        return jsonify({
            "error": str(e)
        }), HTTPStatus.INTERNAL_SERVER_ERROR

# Error handlers
@main.errorhandler(404)
def not_found_error(error):
    return jsonify({
        "error": "Resource not found"
    }), HTTPStatus.NOT_FOUND

@main.errorhandler(500)
def internal_error(error):
    db.session.rollback()  # Roll back db session in case of error
    return jsonify({
        "error": "Internal server error"
    }), HTTPStatus.INTERNAL_SERVER_ERROR