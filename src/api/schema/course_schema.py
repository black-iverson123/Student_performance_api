from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow import fields
from src.api.models.course import Course
from src.api.utils.database import db

class CourseSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Course
        load_instance = True
        sqla_session = db.session
        include_relationships = True
        unknown = 'exclude'

    id = fields.Int(dump_only=True)
    course_title = fields.String(required=True)
    course_code = fields.String(required=True)
    passing_grade = fields.Integer()
    school_id = fields.String(required=False)
    created_by = fields.String(required=False)

    grades = fields.Nested("GradeSchema", many=True, exclude=("course", "id", "student_id"))
