"""
Admin Schema
=============

This module defines the Marshmallow schema used for serializing and 
deserializing the `Admin` model. The schema facilitates data validation,
JSON transformation, and structured API responses.

Purpose:
    - Validate incoming payloads when creating or updating Admin accounts.
    - Serialize Admin model instances into JSON for API responses.
    - Control which fields are exposed (e.g., hide `id` on input, 
      allow `school_id` to be read-only).

Schema:
    AdminSchema

Configuration:
    model (Admin):
        The SQLAlchemy model the schema serializes/deserializes.

    load_instance (True):
        Automatically loads data into an Admin model object.

    sqla_session (db.session):
        SQLAlchemy session used during serialization.

    include_relationships (True):
        Ensures related models are included in the dump if needed.

    ordered (True):
        Ensures serialized fields follow the declared order.

Fields:
    id (Int, dump_only=True):
        Automatically generated primary key. Excluded from input.

    username (String, required=True):
        Admin’s username. Must be unique.

    email (String, required=True):
        Contact and login email. Must be unique.

    password (String, required=True):
        Hashed password. Raw passwords should not be returned to clients.

    school_name (String, required=True):
        Full name of the school the admin manages.

    school_acronym (String, required=True):
        Short code used to generate school identifiers.

    school_id (String, dump_only=True):
        Unique school identifier generated automatically by the Admin model.

Usage Example:
    schema = AdminSchema()
    admin_json = schema.dump(admin_instance)
    admin_obj = schema.load(request.json)

Notes:
    - Never expose plaintext passwords in API responses.
    - Use this schema to validate admin registration and admin retrieval endpoints.
"""


from src.api.models.admin import Admin
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow import fields
from src.api.utils.database import db

class AdminSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Admin
        load_instance = True
        sqla_session = db.session
        include_relationships = True
        ordered = True
 
    id = fields.Int(dump_only=True)
    username = fields.String(required=True)
    email = fields.String(required=True)
    password = fields.String(required=True)
    school_name = fields.String(required=True)
    school_acronym = fields.String(required=True)
    school_id = fields.String(dump_only=True) 
