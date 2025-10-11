from api.models.course import Course
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from api.schema.grade_schema import GradeSchema
from marshmallow import fields
from api.utils.database import db

class CourseSchema(SQLAlchemyAutoSchema):
    class Meta(SQLAlchemyAutoSchema.Meta):
        model = Course
        load_instance = True
        sqla_session = db.session
        include_relationships = True  #allowing relationships
        include_fk = True       #including Foreign keys if any

    id = fields.Int(dump_only=True)
    course_title = fields.String(required=True)
    course_code = fields.String(required=True)
    passing_grade = fields.Integer
    
    #This fetches all associated scores from the database to the course
    grades = fields.Nested(GradeSchema, many=True)
