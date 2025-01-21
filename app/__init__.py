from flask import Flask
import requests

def create_app():
    app = Flask(__name__)

    # You can add additional configuration here, such as:
    app.config.from_object('config.Config')

    # Register routes
    from .routes import main
    app.register_blueprint(main)

    return app
