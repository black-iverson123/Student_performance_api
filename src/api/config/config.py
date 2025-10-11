import os
from dotenv import load_dotenv

load_dotenv()

class Config(object):
    SECRET_KEY = os.getenv("SECRET_KEY")
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
    SQL_TRACK_MODIFICATIONS = os.getenv("SQLALCHEMY_TRACK_MODIFICATIONS")
    SECURITY_PASSWORD_SALT = os.getenv("SECURITY_PASSWORD_SALT")

class DevelopmentConfig(Config):
    DEBUG = os.getenv("DEBUG")
    SQLALCHEMY_DATABASE_URI = os.getenv("SQLALCHEMY_DEV_DATABASE_URI")

class TestingConfig(config):
    DEBUG = os.getenv("DEBUG")
    SQLALCHEMY_DATABASE_URI = os.getenv("SQLALCHEMY_TEST_DATABASE_URI")

