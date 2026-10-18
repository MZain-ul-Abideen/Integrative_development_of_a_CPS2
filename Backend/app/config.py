
# app/config.py
import os
from dotenv import load_dotenv

load_dotenv()

# Database configuration
SQLALCHEMY_DATABASE_URI = os.getenv(
    "DATABASE_URL",
    "mysql+pymysql://myuser:mypassword@localhost/mydatabase"
)
SQLALCHEMY_TRACK_MODIFICATIONS = False

# Email configuration
SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY")
MAIL_DEFAULT_SENDER = os.getenv("MAIL_DEFAULT_SENDER")
