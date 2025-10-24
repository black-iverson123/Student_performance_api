import os
from flask import Flask, request, render_template
from src.api.config.config import DevelopmentConfig, TestingConfig
from src.api.utils.database import db
from src.api.routes.courses import course_routes
from src.api.routes.grades import grade_routes
from src.api.routes.students import student_routes
from src.api.routes.admin import admin_routes
from src.api.models import student, course, grade, admin
from src.api.utils.responses import response_with
from src.api.utils import responses as resp
from src.api.utils.responses import data
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from dotenv import load_dotenv

load_dotenv()

def create_app(config):
    app = Flask(__name__, template_folder="src/templates", static_folder="src/static")

    app.register_blueprint(course_routes, url_prefix="/api/courses")
    app.register_blueprint(grade_routes, url_prefix="/api/grades")
    app.register_blueprint(student_routes, url_prefix="/api/students")
    app.register_blueprint(admin_routes, url_prefix="/api/admin")

    if os.getenv("FLASK_ENV") == "development":
        app_config = DevelopmentConfig()
    if os.getenv("FLASK_ENV") == "testing":
        app_config = TestingConfig()
    
    app.config.from_object(app_config)

    db.init_app(app)
    print("Loaded JWT_SECRET_KEY:", app.config["JWT_SECRET_KEY"])
    jwt = JWTManager(app)
    app.config['JWT_VERIFY_SUB'] = False
    migrate = Migrate(app, db)

    with app.app_context():
        db.create_all()

    #Just to show the app is live
    @app.route('/')
    def index():
        # Serve JSON type response if API client is used
        if request.accept_mimetypes.accept_json and not request.accept_mimetypes.accept_html:
            return response_with(resp.SUCCESS_200, value={"data":data}, message="Welcome!!!!")
            #return jsonify(data)
    
        # Render html page
        return render_template("index.htm", **data)


    # Handle missing token
    @jwt.unauthorized_loader
    def missing_token_callback(error):
        return response_with(resp.SERVER_ERROR_401, message="Missing authorization header. Please log in.")

    # Handle expired access token
    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
         return response_with(resp.SERVER_ERROR_401, message="Access token has expired. Please refresh your token")

    # Handle invalid token
    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        return response_with(resp.SERVER_ERROR_422, message=f"Invalid token. Please log in again. Details {error}")

        
    return app

app=create_app(None)

if __name__ == "__main__":
    app.run(port=os.getenv("FLASK_RUN_PORT"), host=os.getenv("FLASK_RUN_HOST"))