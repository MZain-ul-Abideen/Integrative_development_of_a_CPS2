import os

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "mysecretkey")
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://myuser:mypassword@localhost/mydatabase"

    SQLALCHEMY_TRACK_MODIFICATIONS = False
