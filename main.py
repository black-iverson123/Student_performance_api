import os
from flask import Flask, request, render_template, jsonify
from src.api.config.config import DevelopmentConfig, TestingConfig
from src.api.utils.database import db
from src.api.routes.courses import course_routes
from src.api.models import Student, Course, Grade
from src.api.utils.responses import data
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from dotenv import load_dotenv

load_dotenv()

def create_app(config):
    app = Flask(__name__, template_folder="src/templates", static_folder="src/static")

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

    #Just to show the app is live
    @app.route('/')
    def index():
        # Serve JSON type response if API client
        if request.accept_mimetypes.accept_json and not request.accept_mimetypes.accept_html:
            return jsonify(data)
    
        # Render html page
        return render_template("index.htm", **data)
    
    return app

app=create_app(None)

if __name__ == "__main__":
    app.run(port=os.getenv("FLASK_RUN_PORT"), host=os.getenv("FLASK_RUN_HOST"))