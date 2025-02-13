from .extensions import db

class Service(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)

    def __repr__(self):
        return f"Service('{self.name}')"

class Rule(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)  # Unique name for the trigger
    service_id = db.Column(db.Integer, db.ForeignKey('service.id'), nullable=False)
    condition = db.Column(db.String(500), nullable=False)  # e.g., "inside_temperature > 20"
    email_body = db.Column(db.Text, nullable=True)  # User-defined email body

    service = db.relationship('Service', backref='rules')

    def __repr__(self):
        return f"Rule('{self.name}', '{self.condition}')"

class Action(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    service_id = db.Column(db.Integer, db.ForeignKey('service.id'), nullable=False)
    action_type = db.Column(db.String(100), nullable=False)  # e.g., "Send Email", "Toggle LED"
    parameters = db.Column(db.JSON, nullable=True)  # Store action-specific parameters

    service = db.relationship('Service', backref='actions')

    def __repr__(self):
        return f"Action('{self.name}', '{self.action_type}')"

class TriggerActionLink(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    rule_id = db.Column(db.Integer, db.ForeignKey('rule.id'), nullable=False)
    action_id = db.Column(db.Integer, db.ForeignKey('action.id'), nullable=False)

    rule = db.relationship('Rule', backref='trigger_action_links')
    action = db.relationship('Action', backref='trigger_action_links')

    def __repr__(self):
        return f"TriggerActionLink(Rule='{self.rule.name}', Action='{self.action.name}')"