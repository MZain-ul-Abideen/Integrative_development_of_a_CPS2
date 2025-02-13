from flask import Flask
from flask_migrate import Migrate
from dotenv import load_dotenv
import os
from .extensions import db
from .services.timer_service import start_timer_service
from .services.notification_service import NotificationService

load_dotenv()

def create_app():
    app = Flask(__name__)
    
    app.config.from_pyfile('config.py')
    app.config['WEATHERAPI_API_KEY'] = os.getenv('WEATHERAPI_API_KEY')
    
    db.init_app(app)
    
    # Initialize Flask-Migrate
    migrate = Migrate()
    migrate.init_app(app, db)
    
    # Initialize NotificationService with the app
    global notification_service
    notification_service = NotificationService(app)  # Create a global instance
    
    # Register blueprints
    from .routes import main_routes
    app.register_blueprint(main_routes)
    
    # Start the timer service
    start_timer_service(app)
    
    return app