"""
Grade Schema
=============

This module defines the Marshmallow schema for serializing and deserializing
the `Grade` SQLAlchemy model. It is used across the API for validating
incoming grade data and formatting outgoing JSON responses.

Purpose:
    - Validate and load request data when creating or updating grade entries.
    - Serialize Grade model instances into structured JSON.
    - Expose related student and course information in a controlled way.
    - Enforce strict field handling by excluding unknown fields.

Schema:
    GradeSchema

Configuration:
    model (Grade):
        SQLAlchemy Grade model that this schema maps to.

    load_instance (True):
        Automatically converts validated input into a Grade model instance.

    sqla_session (db.session):
        SQLAlchemy session used during schema load/dump operations.

    include_fk (True):
        Includes foreign key fields in the serialized output.

    unknown ('exclude'):
        Silently drops any unexpected fields from incoming requests.

Fields:
    id (Int, dump_only=True):
        Auto-incrementing grade identifier; excluded from input.

    student (Nested StudentSchema, dump_only=True):
        Contains firstname, lastname, and email of the student.
        Read-only; cannot be supplied during creation or update.

    course (Nested CourseSchema, dump_only=True):
        Contains course_code and course_title of the associated course.
        Read-only; cannot be supplied during creation or update.

    score (Float, required=True):
        Numeric score assigned to the student for the course.

    library_hours (Integer, required=True):
        Number of library hours recorded for the student.

    attendance (Integer, required=True):
        Number of attended sessions for the course.

    status (String, required=True):
        Grade status, e.g., "Passed" or "Failed".

    term (String, required=True):
        Academic term for the grade entry.

    session_year (String, required=True):
        Academic session or year, e.g., "2024/2025".

    student_id (Int, load_only=True, required=True):
        Foreign key to identify the student when creating/updating a grade.

    course_id (Int, load_only=True, required=True):
        Foreign key to identify the course when creating/updating a grade.

    school_id (String, load_only=True, required=True):
        Foreign key to associate the grade with a school.

Usage Example:
    schema = GradeSchema()
    serialized = schema.dump(grade_instance)
    obj = schema.load(request.json)

Notes:
    - student_id, course_id, and school_id are required for POST/PUT requests.
    - Nested student and course data is read-only and should not be supplied.
"""


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
        unknown = "exclude"

    id = fields.Int(dump_only=True)
    student = fields.Nested("StudentSchema", only=("firstname", "lastname", "email"), dump_only=True)
    course = fields.Nested("CourseSchema", only=("course_code", "course_title"), dump_only=True)
    score = auto_field(required=True)
    library_hours = fields.Integer(required=True)
    attendance = fields.Integer(required=True)
    status = fields.String(required=True)
    term = fields.String(required=True)
    session_year = fields.String(required=True)
    student_id = fields.Int(load_only=True, required=True)
    course_id = fields.Int(load_only=True, required=True)
    school_id = fields.String(load_only=True, required=True)
