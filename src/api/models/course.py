"""
Course Model
============

This module defines the `Course` SQLAlchemy model, which represents an academic
course offered by a school. Each course belongs to a school and may have 
multiple grade records associated with it.

Model Purpose:
    - Store metadata about each course (title, code, passing grade).
    - Link grades to their corresponding course through a one-to-many relationship.
    - Enforce unique course codes within the system.

Table Name:
    course

Fields:
    id (Integer, PK):
        Auto-incrementing primary key.

    course_title (String(50)):
        Descriptive title of the course (e.g., "Mathematics").

    course_code (String(8), unique, required):
        Unique shorthand identifier for the course (e.g., "MTH101").
        Automatically converted to uppercase and stripped of whitespace.

    passing_grade (SmallInteger, required):
        Minimum score required for a student to pass the course.

    school_id (String(200), FK -> admin.school_id):
        Identifies which school the course belongs to.

Relationships:
    grades (relationship -> Grade):
        One-to-many relationship associating all grade records with this course.

Methods:
    __init__(course_title, course_code, passing_grade, school_id):
        Initializes a new Course instance with validated attributes.

    create():
        Adds the course to the session and commits it to the database.

Usage Example:
    course = Course(
        course_title="Mathematics",
        course_code="MTH101",
        passing_grade=40,
        school_id="SCHOOL_abc123"
    )
    course.create()
"""


from src.api.utils.database import db


class Course(db.Model):
    __tablename__ = "course"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    course_title = db.Column(db.String(50))
    course_code = db.Column(db.String(8), unique=True, nullable=False)
    passing_grade = db.Column(db.SmallInteger, nullable=False)
    grades = db.relationship("Grade", backref="course", lazy=True) 
    school_id = db.Column(db.String(200), db.ForeignKey('admin.school_id'), nullable=False)

    def __init__(self, course_title, course_code, passing_grade, school_id):
        self.course_title = course_title
        self.course_code = course_code.upper().strip()
        self.passing_grade = passing_grade
        self.school_id = school_id
    
    def create(self):
        db.session.add(self)
        db.session.commit()
        return self