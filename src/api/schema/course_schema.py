"""
Course Schema
==============

This module defines the Marshmallow schema responsible for serializing and
deserializing the `Course` SQLAlchemy model. It is used across the API for
validating incoming course data and formatting outgoing JSON responses.

Purpose:
    - Validate and load request data when creating or updating course entries.
    - Serialize Course model instances into structured JSON.
    - Control exposure of related objects (e.g., grades belonging to a course).
    - Enforce strict field handling by excluding unknown fields.

Schema:
    CourseSchema

Configuration:
    model (Course):
        SQLAlchemy Course model that this schema maps to.

    load_instance (True):
        Automatically converts validated input into a Course model instance.

    sqla_session (db.session):
        SQLAlchemy session used during schema load/dump operations.

    include_relationships (True):
        Allows nested output of related Grade objects.

    unknown ('exclude'):
        Silently drops any unexpected fields from incoming requests.

Fields:
    id (Int, dump_only=True):
        Auto-incrementing course identifier; excluded from input.

    course_title (String, required=True):
        Descriptive title of the course.

    course_code (String, required=True):
        Unique alphanumeric code used to identify the course.

    passing_grade (Integer):
        Minimum score required for students to pass the course.

    school_id (String, optional):
        School identifier linking the course to its admin.

    created_by (String, optional):
        Tracks which admin or user created the course.

    grades (Nested GradeSchema, many=True):
        List of grades associated with the course. Nested objects exclude:
            - course (to prevent recursion)
            - id
            - student_id

Usage Example:
    schema = CourseSchema()
    serialized = schema.dump(course_instance)
    obj = schema.load(request.json)

Notes:
    - Always validate course codes (uniqueness and formatting) at the model or service level.
    - Nested grade data is read-only and should not be supplied during course creation.
"""



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
