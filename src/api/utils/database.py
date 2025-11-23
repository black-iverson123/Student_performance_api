"""
Database Initialization Module
==============================

This module initializes the SQLAlchemy instance used for database interactions
throughout the application. The `db` object should be imported and used in
models, routes, and other parts of the application that require database access.

Usage:
    from src.api.utils.database import db
"""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()