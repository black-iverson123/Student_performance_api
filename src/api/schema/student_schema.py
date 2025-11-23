"""
Student Schema
==============

This module defines the Marshmallow schema for serializing and deserializing
the `Student` SQLAlchemy model. It is used throughout the API for validating
incoming student data and formatting outgoing JSON responses.

Purpose:
    - Validate and load request data when creating or updating student records.
    - Serialize Student model instances into structured JSON.
    - Expose related grades and course performance in a controlled way.

Schema:
    StudentSchema

Configuration:
    model (Student):
        SQLAlchemy Student model that this schema maps to.

    load_instance (True):
        Automatically converts validated input into a Student model instance.

    sqla_session (db.session):
        SQLAlchemy session used during schema load/dump operations.

    include_relationships (True):
        Includes relationships such as 'grades' when serializing data.

Fields:
    id (Int, dump_only=True):
        Auto-incrementing student identifier; excluded from input.

    firstname (String, required=True):
        Student's first name.

    lastname (String, required=True):
        Student's last name.

    email (String, required=True):
        Student's email address; must be unique.

    school_id (String, load_only=True):
        Foreign key to associate the student with a school.
        Required for creating/updating records but excluded from output.

    is_active (Boolean, load_default=True):
        Indicates whether the student is currently active.

    grades (Nested GradeSchema, many=True):
        List of the student's grades, including course info and performance.
        Excludes the nested 'student' field to prevent circular references.

Usage Example:
    schema = StudentSchema()
    serialized = schema.dump(student_instance)
    obj = schema.load(request.json)

Notes:
    - 'grades' is read-only when loading data; only used for serialization.
    - 'school_id' must be provided when creating or updating student records.
"""


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
    school_id = fields.String(load_only=True)
    is_active = fields.Boolean(load_default=True)
    # Each grade shows course info and performance
    grades = fields.Nested("GradeSchema", many=True, exclude=("student",))
