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

    id = fields.Int(dump_only=True)
    course_title = fields.String(required=True)
    course_code = fields.String(required=True)
    passing_grade = fields.Integer()

    # Include all grades related to this course
    grades = fields.Nested("GradeSchema", many=True, exclude=("course", "id", "student_id"))
