from flask import Blueprint, request, jsonify
from .extensions import db
from .models import Service, Rule, Action, TriggerActionLink
from .services.sensor_simulator import fetch_sensor_data
from .services.api_client import fetch_weather_data
from .services.notification_service import notification_service

# Create a Blueprint for the main routes
main_routes = Blueprint('main', __name__)

# -------------------
# Service Management
# -------------------

@main_routes.route('/services', methods=['POST'])
def create_service():
    """
    Create a new service.
    """
    data = request.get_json()
    if not data or 'name' not in data:
        return jsonify({"error": "Service name is required"}), 400

    existing_service = Service.query.filter_by(name=data['name']).first()
    if existing_service:
        return jsonify({"error": "Service already exists"}), 400

    new_service = Service(name=data['name'])

    try:
        db.session.add(new_service)
        db.session.commit()
        return jsonify({
            "message": "Service created successfully",
            "service": {
                "id": new_service.id,
                "name": new_service.name
            }
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


@main_routes.route('/services', methods=['GET'])
def list_services():
    """
    List all services.
    """
    try:
        services = Service.query.all()
        service_list = [{
            "id": service.id,
            "name": service.name
        } for service in services]
        return jsonify(service_list), 200
    except Exception as e:
        print(f"Error fetching services: {e}")
        return jsonify({"error": "Failed to fetch services"}), 500


# -------------------
# Rule (Trigger) Management
# -------------------

@main_routes.route('/rules', methods=['POST'])
def create_rule():
    """
    Create a new rule (trigger).
    """
    data = request.get_json()
    if not data or 'service_id' not in data or 'name' not in data or 'condition' not in data:
        return jsonify({"error": "Service ID, name, and condition are required"}), 400

    service = Service.query.get(data['service_id'])
    if not service:
        return jsonify({"error": "Service not found"}), 404

    new_rule = Rule(
        name=data['name'],
        service_id=data['service_id'],
        condition=data['condition'],
        email_body=data.get('email_body')  # Optional for non-email rules
    )

    try:
        db.session.add(new_rule)
        db.session.commit()
        return jsonify({
            "message": "Rule created successfully",
            "rule": {
                "id": new_rule.id,
                "name": new_rule.name,
                "condition": new_rule.condition,
                "email_body": new_rule.email_body,
                "service": {
                    "id": service.id,
                    "name": service.name
                }
            }
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


@main_routes.route('/rules', methods=['GET'])
def list_rules():
    """
    List all created rules.
    """
    try:
        rules = Rule.query.all()
        rule_list = [{
            "id": rule.id,
            "name": rule.name,
            "condition": rule.condition,
            "email_body": rule.email_body,
            "service": {
                "id": rule.service.id,
                "name": rule.service.name
            }
        } for rule in rules]
        return jsonify(rule_list), 200
    except Exception as e:
        print(f"Error fetching rules: {e}")
        return jsonify({"error": "Failed to fetch rules"}), 500


# -------------------
# Action Management
# -------------------

@main_routes.route('/actions', methods=['POST'])
def create_action():
    """
    Create a new action.
    """
    data = request.get_json()
    if not data or 'service_id' not in data or 'name' not in data or 'action_type' not in data:
        return jsonify({"error": "Service ID, name, and action type are required"}), 400

    service = Service.query.get(data['service_id'])
    if not service:
        return jsonify({"error": "Service not found"}), 404

    new_action = Action(
        name=data['name'],
        service_id=data['service_id'],
        action_type=data['action_type'],
        parameters=data.get('parameters', {})  # Store action-specific parameters
    )

    try:
        db.session.add(new_action)
        db.session.commit()
        return jsonify({
            "message": "Action created successfully",
            "action": {
                "id": new_action.id,
                "name": new_action.name,
                "action_type": new_action.action_type,
                "parameters": new_action.parameters,
                "service": {
                    "id": service.id,
                    "name": service.name
                }
            }
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


@main_routes.route('/actions', methods=['GET'])
def list_actions():
    """
    List all created actions.
    """
    try:
        actions = Action.query.all()
        action_list = [{
            "id": action.id,
            "name": action.name,
            "action_type": action.action_type,
            "parameters": action.parameters,
            "service": {
                "id": action.service.id,
                "name": action.service.name
            }
        } for action in actions]
        return jsonify(action_list), 200
    except Exception as e:
        print(f"Error fetching actions: {e}")
        return jsonify({"error": "Failed to fetch actions"}), 500


# -------------------
# Link Rules and Actions
# -------------------

@main_routes.route('/link-rule-action', methods=['POST'])
def link_rule_action():
    """
    Link a rule (trigger) with an action.
    """
    data = request.get_json()
    if not data or 'rule_id' not in data or 'action_id' not in data:
        return jsonify({"error": "Rule ID and Action ID are required"}), 400

    rule = Rule.query.get(data['rule_id'])
    if not rule:
        return jsonify({"error": "Rule not found"}), 404

    action = Action.query.get(data['action_id'])
    if not action:
        return jsonify({"error": "Action not found"}), 404

    new_link = TriggerActionLink(rule_id=rule.id, action_id=action.id)

    try:
        db.session.add(new_link)
        db.session.commit()
        return jsonify({
            "message": "Rule and action linked successfully",
            "link": {
                "rule_id": rule.id,
                "rule_name": rule.name,
                "action_id": action.id,
                "action_name": action.name
            }
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


# -------------------
# Debugging Routes
# -------------------

@main_routes.route('/debug/sensor', methods=['GET'])
def debug_sensor():
    """
    Fetch and display sensor and weather data for debugging.
    """
    sensor_data = fetch_sensor_data() or {}
    weather_data = fetch_weather_data() or {}

    combined_data = {
        **sensor_data,
        **weather_data,
        "inside_temperature": sensor_data.get("inside_temperature", "N/A"),  # Fallback value
        "weather_condition": weather_data.get("weather_condition", "N/A")   # Fallback value
    }

    return jsonify({
        "sensor_data": sensor_data,
        "weather_data": weather_data,
        "combined": combined_data
    }), 200


# -------------------
# Test Notification Route
# -------------------

@main_routes.route('/send-notification', methods=['POST'])
def send_test_notification():
    """
    Send a test notification with dynamic data.
    """
    data = request.get_json()

    if not data or 'emailBody' not in data or 'subject' not in data or 'recipient' not in data:
        return jsonify({"error": "Email body, subject, and recipient are required"}), 400

    email_body = data.get("emailBody")
    subject = data.get("subject")
    recipient = data.get("recipient")
    notification_type = data.get("notification_type", "email")

    try:
        # Replace placeholders in the email body with actual values
        inside_temperature = data.get("inside_temperature", "N/A")
        outside_forecast = data.get("outside_forecast", "N/A")
        email_body = email_body.format(
            inside_temperature=inside_temperature,
            outside_forecast=outside_forecast
        )

        # Call the instance method on notification_service
        success = notification_service.send_notification(
            data={
                "emailBody": email_body,
                "subject": subject,
                "inside_temperature": inside_temperature,
                "outside_forecast": outside_forecast
            },
            notification_type=notification_type,
            recipient=recipient
        )

        if success:
            return jsonify({"message": "Notification sent successfully"}), 200
        else:
            return jsonify({"error": "Failed to send notification"}), 500

    except KeyError as e:
        return jsonify({"error": f"Missing key in data: {e}"}), 400

    except Exception as e:
        return jsonify({"error": str(e)}), 500