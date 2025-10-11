from api.models.grade import Grade
from api.schema.course_schema import CourseSchema
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow import fields
from api.utils.database import db


class GradeSchema(SQLAlchemyAutoSchema):
    class Meta(SQLAlchemyAutoSchema.Meta):
        model = Grade
        load_instance = True
        sqla_session = db.session

    
    id = fields.Int(dump_only=True)
    student_id = fields.String(required=True)
    course_id = fields.String(required=True)
    score = fields.String(required=True)
    status = fields.Nested(CourseSchema, many=True, only=['course_title','course_code','passing_grade','grades'])
