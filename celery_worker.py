"""
Celery Configuration and Integration with Flask Application Context.

This module initializes and configures a Celery instance for asynchronous
task processing within the Students Performance Manager API. It sets up
Redis as both the message broker and result backend, and ensures Celery
tasks have access to the Flask application context when executed.

Key Responsibilities:
---------------------
1. Celery Initialization:
   - Creates a Celery application named "tasks"
   - Configures Redis as:
        • Message broker → redis://localhost:6379/0
        • Result backend → redis://localhost:637:6379/0
   - Allows asynchronous execution of long-running tasks such as
     grade imports or background analytics.

2. Flask Context Binding:
   - Celery tasks normally run outside Flask.
   - `init_celery(app)` wraps each task in Flask's `app.app_context()`
     so that tasks can:
        • Access SQLAlchemy models  
        • Use database sessions  
        • Access app configuration  
        • Use any Flask extensions (JWT, current_app, etc.)

3. Usage Pattern:
   - Import and initialize Celery inside the Flask application factory:
        from celery_worker import init_celery
        init_celery(app)

   - Create tasks in separate modules and decorate them with:
        @celery.task

4. Benefits:
   - Prevents circular imports.
   - Ensures clean, manageable background job architecture.
   - Keeps Celery configuration separate from the Flask factory for
     better modularity and maintainability.

This module ensures that Celery and Flask work together seamlessly
when executing asynchronous background tasks.
"""


from celery import Celery

celery = Celery(
    "tasks",
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/0"
)

# We'll attach Flask context later in tasks
def init_celery(app):
    celery.conf.update(app.config)

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery
