from flask import Flask
from flask_migrate import Migrate
from dotenv import load_dotenv
import os
from .extensions import db
from .services.timer_service import start_timer_service
from .services.notification_service import NotificationService

from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv
from .extensions import db
from .routes import main_routes
from .services.timer_service import start_timer_service

load_dotenv()

def create_app():
    app = Flask(__name__)
    
    # Load configuration
    app.config.from_pyfile('config.py')
    app.config['WEATHERAPI_API_KEY'] = os.getenv('WEATHERAPI_API_KEY')

    # Initialize database
    db.init_app(app)
    migrate = Migrate(app, db)
    # Enable CORS for all routes
    CORS(app, resources={r"/*": {"origins": "http://localhost:8080"}})  # Allow requests from localhost:8080

    # Register blueprints
    app.register_blueprint(main_routes)

    # Start the timer service
    start_timer_service(app)

    return app