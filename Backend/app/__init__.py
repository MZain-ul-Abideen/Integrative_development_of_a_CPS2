from flask import Flask
from flask_migrate import Migrate
from flask_cors import CORS
from dotenv import load_dotenv
from .extensions import db
from .routes import main_routes
from .services.timer_service import start_timer_service
from .services.notification_service import NotificationService  # Import the NotificationService
import os

load_dotenv()

def create_app():
    app = Flask(__name__)
    
    # Load configuration
    app.config.from_pyfile('config.py')
    app.config['WEATHERAPI_API_KEY'] = os.getenv('WEATHERAPI_API_KEY')
    
    # Initialize database
    db.init_app(app)
    migrate = Migrate(app, db)
    
    # Enable CORS with explicit method permissions
    CORS(app, resources={
        r"/*": {
            "origins": "http://localhost:8080",
            "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            "allow_headers": ["Content-Type", "Authorization"]
        }
    })
    
    # Register blueprints
    app.register_blueprint(main_routes)
    
    # Initialize NotificationService with the app
    app.notification_service = NotificationService(app)  # Store it in the app instance

    # Start the timer service
    start_timer_service(app)
    
    return app