import os
from flask import Flask
from src.api.config.config import DevelopmentConfig, TestingConfig
from src.api.utils.database import db
from src.api.routes.courses import course_routes
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from dotenv import load_dotenv

load_dotenv()

def create_app(config):
    app = Flask(__name__)

    app.register_blueprint(course_routes, url_prefix="/api/courses")

    if os.getenv("FLASK_ENV") == "development":
        app_config = DevelopmentConfig()
    if os.getenv("FLASK_ENV") == "testing":
        app_config = TestingConfig()
    
    app.config.from_object(app_config)

    db.init_app(app)
    jwt = JWTManager(app)
    migrate = Migrate(app, db)

    with app.app_context():
        db.create_all()
    

app=create_app(None)

if __name__ == "__main__":
    app.run(port=5000, host="0.0.0.0")