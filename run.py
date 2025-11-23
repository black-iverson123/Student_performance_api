"""
WSGI Entry Point for Production Deployment.

This module exposes the Flask application instance in a format compatible
with WSGI servers such as Gunicorn, uWSGI, Apache mod_wsgi, or Nginx +
uWSGI setups.

Purpose:
--------
- Imports the Flask application object (`app`) from the main application
  module and exposes it as `application`, which is the standard variable
  name expected by most WSGI servers.
- Ensures that the app can run both:
    • In a production context (WSGI server loads `application`)
    • In a fallback standalone mode when executed directly via:
          python wsgi.py

Responsibilities:
-----------------
- Provide a WSGI-compatible callable (`application`)
- Allow direct execution for debugging purposes

Typical Usage:
--------------
Deployment with Gunicorn:
    gunicorn wsgi:application --bind 0.0.0.0:8000 --workers 4

Deployment with uWSGI:
    uwsgi --http :8000 --wsgi-file wsgi.py --callable application

This design cleanly separates development execution from production-grade
WSGI serving, improving portability and deployability.
"""



from main import app as application

if __name__ == "__main__":
    application.run()