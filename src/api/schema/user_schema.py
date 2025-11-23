"""
User Schema
===========

This module defines the Marshmallow schema for the `User` SQLAlchemy model.

Purpose:
    - Validate input data when creating or updating a User.
    - Serialize User model instances into JSON for API responses.
    - Include relationships such as the associated Admin.
    - Provide field-level constraints (e.g., required fields, dump-only fields).

Fields:
    - id: Integer, dump-only, the primary key of the User.
    - firstname: String, required, the first name of the user.
    - lastname: String, required, the last name of the user.
    - email: String, required, unique user email.
    - password: String, required, hashed password.
    - role: String, required, user role (e.g., teacher, admin).
    - school_id: String, required, the associated school's ID.
    - admin_id: Integer, required, foreign key linking to an Admin.
    - is_active: Boolean, defaults to True, indicates whether the user is active.
"""



from src.api.models.user import User
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow import fields
from src.api.utils.database import db

class UserSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = User
        load_instance = True
        sqla_session = db.session
        include_relationships = True
        ordered = True
        unknown = 'exclude'
    
    id = fields.Int(dump_only=True)
    firstname = fields.String(required=True)
    lastname = fields.String(required=True)
    email = fields.String(required=True)
    password = fields.String(required=True)
    role = fields.String(required=True)
    school_id = fields.String(required=True)
    admin_id = fields.Int(required=True)
    is_active = fields.Boolean(load_default=True)