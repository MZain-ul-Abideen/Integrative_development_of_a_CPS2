from .extensions import db

class Service(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)

class Rule(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    service_id = db.Column(db.Integer, db.ForeignKey('service.id'), nullable=False)
    condition = db.Column(db.String(500), nullable=False)  # e.g., "outside_temperature > 20" or "weather_condition == 'Rainy'"
    range_value = db.Column(db.Float, nullable=True)       # For temperature-based rules
    last_executed = db.Column(db.Float, default=0)         # For timer-based rules

    service = db.relationship('Service', backref='rules')

class Action(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    service_id = db.Column(db.Integer, db.ForeignKey('service.id'), nullable=False)
    action_type = db.Column(db.String(100), nullable=False)  # e.g., "Building Automation", "Send Email", "Toggle LED"
    parameters = db.Column(db.JSON, nullable=True)           # Store action-specific parameters

    service = db.relationship('Service', backref='actions')

class TriggerActionLink(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    rule_id = db.Column(db.Integer, db.ForeignKey('rule.id'), nullable=False)
    action_id = db.Column(db.Integer, db.ForeignKey('action.id'), nullable=False)

    rule = db.relationship('Rule', backref='trigger_action_links')
    action = db.relationship('Action', backref='trigger_action_links')