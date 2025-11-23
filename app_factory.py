"""
Application Factory for the Students Performance Manager API.

This module initializes and configures the Flask application using the
application factory pattern. It handles environment-based configuration,
blueprint registration, database initialization, JWT authentication setup,
and error handling for token-related exceptions.

Key Responsibilities:
---------------------
1. Environment-Aware Configuration:
   - Loads configuration from DevelopmentConfig, TestingConfig, or ProductionConfig
     based on the FLASK_ENV environment variable.
   - Loads environment variables using python-dotenv.

2. Blueprint Registration:
   Registers routed modules for different API domains:
     - /api/courses   → Course management
     - /api/grades    → Grade upload, view, updates
     - /api/students  → Student management
     - /api/admin     → Admin and school setup operations
     - /api/users     → User creation, roles, and authentication

3. Database & Migrations:
   - Initializes SQLAlchemy with `db.init_app(app)`
   - Automatically creates all tables on startup
   - Integrates Flask-Migrate for schema version control

4. JWT Authentication:
   - Initializes JWTManager for token-based authentication
   - Provides custom handlers for:
       • Missing tokens
       • Expired tokens
       • Invalid tokens

5. Unified API Response Handling:
   - Uses the global `response_with()` utility and standardized response objects
     from `src.api.utils.responses` for consistent JSON output.

6. Root Route:
   - Returns JSON when API clients request JSON
   - Returns an HTML landing page when accessed via browser

Usage:
------
Import and call `create_app()` with an environment configuration to
obtain the fully configured Flask application instance:

    from app import create_app
    app = create_app("development")

This module serves as the main entry point for the API and ensures that
all components (routes, database, authentication, templates, static files,
and configurations) are properly initialized before the server starts.
"""


import os
from flask import Flask, request, render_template
from src.api.config.config import DevelopmentConfig, TestingConfig, ProductionConfig
from src.api.utils.database import db
from src.api.models import student, course, grade, admin, user
from src.api.utils.responses import response_with
from src.api.utils import responses as resp
from src.api.utils.responses import data
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from flasgger import Swagger
from src.api.utils.swag_tool import swagger_template
from dotenv import load_dotenv

load_dotenv()

def create_app(config):
    app = Flask(__name__, template_folder="src/templates", static_folder="src/static")

    from src.api.routes.courses import course_routes
    from src.api.routes.grades import grade_routes
    from src.api.routes.students import student_routes
    from src.api.routes.admin import admin_routes
    from src.api.routes.user import user_routes
    
    app.register_blueprint(course_routes, url_prefix="/api/courses")
    app.register_blueprint(grade_routes, url_prefix="/api/grades")
    app.register_blueprint(student_routes, url_prefix="/api/students")
    app.register_blueprint(admin_routes, url_prefix="/api/admin")
    app.register_blueprint(user_routes, url_prefix="/api/users")

    if os.environ.get('FLASK_ENV') == 'production':
        app_config = ProductionConfig()
    elif os.environ.get('FLASK_ENV') == 'testing':
        app_config = TestingConfig()
    else:
        app_config = DevelopmentConfig()

    app.config.from_object(app_config)


    #Just to show the app is live
    @app.route('/')
    def index():
        # Serve JSON type response if API client is used
        if request.accept_mimetypes.accept_json and not request.accept_mimetypes.accept_html:
            return response_with(resp.SUCCESS_200, value={"data":data}, message="Welcome!!!!")
            #return jsonify(data)
    
        # Render html page
        return render_template("index.htm", **data)

    jwt = JWTManager(app)
    
    # Handle missing token
    @jwt.unauthorized_loader
    def missing_token_callback(error):
        return response_with(resp.UNAUTHORIZED_401, message="Missing authorization header. Please log in.")

    # Handle expired access token
    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
         return response_with(resp.UNAUTHORIZED_401, message="Access token has expired. Please refresh your token")

    # Handle invalid token
    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        return response_with(resp.UNAUTHORIZED_401, message=f"Invalid token. Please log in again. Details {error}")
    

    db.init_app(app)
    app.config['JWT_VERIFY_SUB'] = False
    migrate = Migrate(app, db)
    Swagger(app, template=swagger_template)

    with app.app_context():
        db.create_all()
            
    return app