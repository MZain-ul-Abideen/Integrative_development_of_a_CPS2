from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Rule(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    trigger_service = db.Column(db.String(50), nullable=False)
    trigger_condition = db.Column(db.String(200), nullable=False)
    action_service = db.Column(db.String(50), nullable=False)
    action_details = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return f"<Rule {self.name}>"