from flask import Blueprint, request, jsonify
from .extensions import db
from .models import Rule, NotificationTemplate
from .services.notification_service import NotificationService
from .services.sensor_simulator import fetch_sensor_data
from .services.api_client import fetch_weather_data

# Create a Blueprint for the main routes
main_routes = Blueprint('main', __name__)

# Notification Template Routes
@main_routes.route('/notification-templates', methods=['POST'])
def create_notification_template():
    """
    Create a new notification template.
    """
    data = request.get_json()
    
    # Validate input
    if not data or 'name' not in data or 'template' not in data:
        return jsonify({"error": "Name and template are required"}), 400
    
    # Check if template already exists
    existing_template = NotificationTemplate.query.filter_by(name=data['name']).first()
    if existing_template:
        return jsonify({"error": "Template with this name already exists"}), 400
    
    # Create new template
    new_template = NotificationTemplate(
        name=data['name'],
        template=data['template']
    )
    
    try:
        db.session.add(new_template)
        db.session.commit()
        return jsonify({
            "message": "Template created successfully",
            "template": {
                "id": new_template.id,
                "name": new_template.name,
                "template": new_template.template
            }
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@main_routes.route('/notification-templates', methods=['GET'])
def list_notification_templates():
    """
    List all notification templates.
    """
    templates = NotificationTemplate.query.all()
    return jsonify([{
        "id": template.id,
        "name": template.name,
        "template": template.template
    } for template in templates])

@main_routes.route('/notification-templates/<int:template_id>', methods=['PUT'])
def update_notification_template(template_id):
    """
    Update an existing notification template.
    """
    data = request.get_json()
    
    # Validate input
    if not data or ('name' not in data and 'template' not in data):
        return jsonify({"error": "Name or template must be provided"}), 400
    
    # Find the template
    template = NotificationTemplate.query.get(template_id)
    if not template:
        return jsonify({"error": "Template not found"}), 404
    
    # Update fields
    if 'name' in data:
        template.name = data['name']
    if 'template' in data:
        template.template = data['template']
    
    try:
        db.session.commit()
        return jsonify({
            "message": "Template updated successfully",
            "template": {
                "id": template.id,
                "name": template.name,
                "template": template.template
            }
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@main_routes.route('/notification-templates/<int:template_id>', methods=['DELETE'])
def delete_notification_template(template_id):
    """
    Delete a notification template.
    """
    template = NotificationTemplate.query.get(template_id)
    if not template:
        return jsonify({"error": "Template not found"}), 404
    
    try:
        db.session.delete(template)
        db.session.commit()
        return jsonify({"message": "Template deleted successfully"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@main_routes.route('/send-notification', methods=['POST'])
def send_test_notification():
    """
    Send a test notification.
    """
    data = request.get_json()
    
    # Validate input
    if not data or 'template_name' not in data:
        return jsonify({"error": "Template name is required"}), 400
    
    # Get notification type (default to print)
    notification_type = data.get('notification_type', 'print')
    
    # Get template data (optional)
    template_data = data.get('template_data', {})
    
    # For email, recipient is required
    if notification_type == 'email':
        if 'recipient' not in data:
            return jsonify({"error": "Recipient email is required for email notifications"}), 400
        recipient = data['recipient']
    else:
        recipient = None
    
    try:
        result = NotificationService.send_notification(
            template_name=data['template_name'],
            data=template_data,
            notification_type=notification_type,
            recipient=recipient
        )
        
        if result:
            return jsonify({"message": "Notification sent successfully"}), 200
        else:
            return jsonify({"error": "Failed to send notification"}), 500
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Rule Management Routes
@main_routes.route('/rules', methods=['GET'])
def get_rules():
    """
    List all rules.
    """
    rules = Rule.query.all()
    return jsonify([{'id': rule.id, 'name': rule.name, 'condition': rule.condition, 'action': rule.action} for rule in rules])

@main_routes.route('/rules', methods=['POST'])
def create_rule():
    """
    Create a new rule.
    """
    data = request.json
    new_rule = Rule(name=data['name'], condition=data['condition'], action=data['action'])
    db.session.add(new_rule)
    db.session.commit()
    return jsonify({'message': 'Rule created successfully', 'id': new_rule.id}), 201

# Debugging Routes
@main_routes.route('/debug/sensor', methods=['GET'])
def debug_sensor():
    """
    Fetch and display sensor and weather data for debugging.
    """
    sensor_data = fetch_sensor_data()
    weather_data = fetch_weather_data()
    
    return jsonify({
        "sensor_data": sensor_data,
        "weather_data": weather_data,
        "combined": {**sensor_data, **weather_data}
    })