from src.api.models.grade import Grade
from src.api.utils.database import db
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, auto_field
from marshmallow import fields



class GradeSchema(SQLAlchemyAutoSchema):
    class Meta(SQLAlchemyAutoSchema.Meta):
        model = Grade
        load_instance = True
        sqla_session = db.session
        include_fk = True
        unknown = 'exclude'

    
    id = fields.Int(dump_only=True)
    student = fields.Nested("StudentSchema", only=("firstname", "lastname", "email"))
    course = fields.Nested("CourseSchema", only=("course_code", "course_title"))
    score = auto_field()
    library_hours = fields.Integer(required=True)
    attendance = fields.Integer(required=True)
    status = fields.String(required=True)
