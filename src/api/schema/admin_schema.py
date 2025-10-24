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