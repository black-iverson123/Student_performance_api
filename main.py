"""
Application Entry Point and Celery Initialization.

This module serves as the main entry point for running the Students
Performance Manager API. It initializes the Flask application using the
central application factory pattern and sets up Celery for asynchronous
task execution within the same application context.

Key Responsibilities:
---------------------
1. Flask Application Bootstrap:
   - Imports and invokes `create_app()` from the application factory.
   - Loads environment-specific configuration automatically using
     environment variables such as:
        • FLASK_ENV
        • FLASK_RUN_PORT
        • FLASK_RUN_HOST

2. Celery Integration:
   - Initializes Celery using `init_celery(app)` so that background
     tasks can run with full Flask application context, including access
     to:
        • Database models and sessions
        • Application configuration
        • Flask extensions (JWT, Migrate, etc.)

3. Local Development Server:
   - When executed directly (`python main.py`), this module starts the
     Flask development server with host/port values loaded from the
     environment.

Usage:
------
- Run the application:
      python main.py

- Start Celery worker in a separate terminal:
      celery -A celery_worker.celery worker --loglevel=info

This module ensures that both the API and Celery workers operate within
the same application configuration and share a consistent execution
environment.
"""


import os
from app_factory import create_app
from celery_worker import init_celery

app = create_app(None)
celery = init_celery(app)

if __name__ == "__main__":
    app.run(port=os.environ.get("FLASK_RUN_PORT"), 
            host=os.environ.get("FLASK_RUN_HOST"))