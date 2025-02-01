import os
from dotenv import load_dotenv

load_dotenv()

# Database configuration
SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'mysql+pymysql://myuser:mypassword@localhost/mydatabase')
SQLALCHEMY_TRACK_MODIFICATIONS = False