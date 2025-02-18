#/app/config.py
import os
from dotenv import load_dotenv

load_dotenv()

# Database configuration
SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'mysql+pymysql://myuser:mypassword@localhost/mydatabase')
SQLALCHEMY_TRACK_MODIFICATIONS = False
SENDGRID_API_KEY='REDACTED_SENDGRID_KEY'
MAIL_DEFAULT_SENDER='mohammadamin.norouzi.2023@gmail.com'