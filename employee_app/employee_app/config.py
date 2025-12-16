import os
from datetime import timedelta

class Config:
    # MySQL Database
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:Anii%40123@localhost:3306/employee_db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = True
    
    # Flask Secret Key
    SECRET_KEY = 'my-flask-secret-key-67890'
    
    # JWT Configuration
    JWT_SECRET_KEY = 'my-super-secret-jwt-key-12345'
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=30)   # Access token expires in 30 mins
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)     # Refresh token expires in 30 days
    JWT_IDENTITY_CLAIM = "sub"  # Ensure JWT identity is treated as string


class DevelopmentConfig(Config):
    DEBUG = True


class ProductionConfig(Config):
    DEBUG = False


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///test.db'

