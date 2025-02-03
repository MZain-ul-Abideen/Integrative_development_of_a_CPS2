from flask import Blueprint, request, jsonify
from .extensions import db
from .models import Rule

main_routes = Blueprint('main', __name__)

@main_routes.route('/rules', methods=['GET'])
def get_rules():
    rules = Rule.query.all()
    return jsonify([{'id': rule.id, 'name': rule.name, 'condition': rule.condition, 'action': rule.action} for rule in rules])

@main_routes.route('/rules', methods=['POST'])
def create_rule():
    data = request.json
    new_rule = Rule(name=data['name'], condition=data['condition'], action=data['action'])
    db.session.add(new_rule)
    db.session.commit()
    return jsonify({'message': 'Rule created successfully', 'id': new_rule.id}), 201

@main_routes.route('/debug/sensor', methods=['GET'])
def debug_sensor():
    from app.services.sensor_simulator import fetch_sensor_data
    from app.services.api_client import fetch_weather_data
    
    sensor_data = fetch_sensor_data()
    weather_data = fetch_weather_data()
    
    return jsonify({
        "sensor_data": sensor_data,
        "weather_data": weather_data,
        "combined": {**sensor_data, **weather_data}
    })