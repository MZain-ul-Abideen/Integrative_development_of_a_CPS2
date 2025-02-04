from .extensions import db

class Rule(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    condition = db.Column(db.String(500), nullable=False)  # e.g., "temperature > 30"
    action = db.Column(db.String(500), nullable=False)  # e.g., "send_notification"
    is_active = db.Column(db.Boolean, default=True)

    def __repr__(self):
        return f"Rule('{self.name}', '{self.condition}', '{self.action}')"
    

class NotificationTemplate(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    template = db.Column(db.Text, nullable=False)
    
    def __repr__(self):
        return f"<NotificationTemplate {self.name}>"