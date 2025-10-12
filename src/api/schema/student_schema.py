from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow import fields
from src.api.models.student import Student
from src.api.utils.database import db

class StudentSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Student
        load_instance = True
        sqla_session = db.session
        include_relationships = True

    id = fields.Int(dump_only=True)
    firstname = fields.String(required=True)
    lastname = fields.String(required=True)
    email = fields.String(required=True)

    # Each grade shows course info and performance
    grades = fields.Nested("GradeSchema", many=True, exclude=("student",))
