"""
Configuration module for the Students Performance Manager API.

This module loads environment variables from a `.env` file and defines
different configuration classes for various environments: production, 
development, and testing. These classes centralize all settings such as
database URIs, secret keys, and optional email or file upload configurations.

Classes:
    config: Base configuration class with default settings.
    ProductionConfig: Configuration settings for production environment.
    DevelopmentConfig: Configuration settings for development environment.
    TestingConfig: Configuration settings for testing environment.

Environment Variables Used:
    - DATABASE_URL: Production database URI
    - DEV_DATABASE_URL: Development database URI
    - TEST_DATABASE_URL: Testing database URI
    - SECRET_KEY: Flask secret key for session management
    - JWT_SECRET_KEY: Secret key for JWT authentication
    - SECURITY_PASSWORD_SALT: Salt for password hashing
    - MAIL_*: Optional email server settings (commented out - Feature may be added later)
    - UPLOAD_FOLDER: Optional file upload folder (commented out - Feature may be added later)
"""



import os
from dotenv import load_dotenv

# Load variables from .env file
load_dotenv()

class config(object):
    DEBUG = False
    TESTING = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class ProductionConfig(config):
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")
    SECRET_KEY = os.getenv("SECRET_KEY")
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
    SECURITY_PASSWORD_SALT = os.getenv("SECURITY_PASSWORD_SALT")
    #MAIL_DEFAULT_SENDER = os.getenv("MAIL_DEFAULT_SENDER")
    #MAIL_SERVER = os.getenv("MAIL_SERVER")
    #MAIL_PORT = int(os.getenv("MAIL_PORT", 465))
    #MAIL_USERNAME = os.getenv("MAIL_USERNAME")
    #MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")
    #MAIL_USE_TLS = os.getenv("MAIL_USE_TLS", "False").lower() == "true"
    #MAIL_USE_SSL = os.getenv("MAIL_USE_SSL", "True").lower() == "true"
    #UPLOAD_FOLDER = os.getenv("UPLOAD_FOLDER", "images")


class DevelopmentConfig(config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.getenv("DEV_DATABASE_URL")
    SECRET_KEY = os.getenv("SECRET_KEY")
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
    SECURITY_PASSWORD_SALT = os.getenv("SECURITY_PASSWORD_SALT")
    #MAIL_DEFAULT_SENDER = os.getenv("MAIL_DEFAULT_SENDER")
    #MAIL_SERVER = os.getenv("MAIL_SERVER")
    #MAIL_PORT = int(os.getenv("MAIL_PORT", 465))
    #MAIL_USERNAME = os.getenv("MAIL_USERNAME")
    #MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")
    #MAIL_USE_TLS = os.getenv("MAIL_USE_TLS", "False").lower() == "true"
    #MAIL_USE_SSL = os.getenv("MAIL_USE_SSL", "True").lower() == "true"
    #UPLOAD_FOLDER = os.getenv("UPLOAD_FOLDER", "images")


class TestingConfig(config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.getenv("TEST_DATABASE_URL")
    SECRET_KEY = os.getenv("SECRET_KEY")
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
    SECURITY_PASSWORD_SALT = os.getenv("SECURITY_PASSWORD_SALT")
    #MAIL_DEFAULT_SENDER = os.getenv("MAIL_DEFAULT_SENDER")
    #MAIL_PORT = int(os.getenv("MAIL_PORT", 465))
    #MAIL_USERNAME = os.getenv("MAIL_USERNAME")
    #AIL_PASSWORD = os.getenv("MAIL_PASSWORD")
    #MAIL_USE_TLS = os.getenv("MAIL_USE_TLS", "False").lower() == "true"
    #MAIL_USE_SSL = os.getenv("MAIL_USE_SSL", "True").lower() == "true"
    #UPLOAD_FOLDER = os.getenv("UPLOAD_FOLDER", "images")
