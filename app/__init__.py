from flask import Flask
from .models import db
from .routes import main as main_blueprint  # Import the Blueprint

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')

    # Initialize the database
    db.init_app(app)

    # Register the Blueprint
    app.register_blueprint(main_blueprint)

    with app.app_context():
        db.create_all()  # Create tables if they don't exist

    return app