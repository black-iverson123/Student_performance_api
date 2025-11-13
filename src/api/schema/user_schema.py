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