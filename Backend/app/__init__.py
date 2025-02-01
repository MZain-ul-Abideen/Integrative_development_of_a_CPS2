from flask import Flask
from flask_migrate import Migrate
from dotenv import load_dotenv
import os
from .extensions import db
from .services.timer_service import start_timer_service
from .routes import main_routes

# Load environment variables from .env file
load_dotenv()

def create_app():
    app = Flask(__name__)
    
    app.config.from_pyfile('config.py')
    app.config['WEATHERAPI_API_KEY'] = os.getenv('WEATHERAPI_API_KEY')
    
    db.init_app(app)
    
    # Add these lines to initialize Flask-Migrate
    migrate = Migrate()
    migrate.init_app(app, db)
    
    app.register_blueprint(main_routes)
    start_timer_service(app)
    
    return app