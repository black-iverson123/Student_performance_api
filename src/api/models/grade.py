
"""
Grade Model
===========

This module defines the `Grade` SQLAlchemy model, which stores the performance 
and activity records of students in specific courses. Each grade entry represents 
a unique combination of student, course, academic session, and term within a 
particular school.

Model Purpose:
    - Track student performance across subjects (score).
    - Record academic activity metrics such as attendance and library hours.
    - Ensure unique grade records per student/course/session/term.
    - Link grade data to schools through school_id for multi-tenancy.

Table Name:
    grades

Fields:
    id (Integer, PK):
        Auto-incrementing primary identifier.

    student_id (Integer, FK -> student.id):
        Links each grade to the corresponding student.

    course_id (Integer, FK -> course.id):
        Identifies the course the grade belongs to.

    attendance (Integer, required):
        Number of classes attended by the student.

    library_hours (Integer, required):
        Number of hours spent in the library.

    score (Float(4), required):
        Numerical grade/score for the course.

    status (String(10), required):
        Pass/Fail or other status flag set by grading logic.

    session (String(9), required):
        Academic session identifier (e.g., "2023/2024").

    term (String(20), required):
        Term within the session (e.g., "First Term", "Semester 1").

    school_id (String(200), FK -> admin.school_id):
        Associates grade records with a specific school account.

    is_active (Boolean, default=True):
        Marks grade entries that are active or deprecated.

Constraints:
    UniqueConstraint(student_id, course_id, session, term, school_id):
        Ensures that a student cannot have duplicate grade entries for the 
        same course within the same session and term in the same school.

Methods:
    __init__(...):
        Initializes a Grade instance with all required fields.

    create():
        Adds the grade to the database session and commits it.

Usage Example:
    grade = Grade(
        student_id=1,
        course_id=10,
        score=84.5,
        status="Pass",
        school_id="SCH_123456",
        is_active=True,
        attendance=28,
        library_hours=12,
        session="2023/2024",
        term="First Term"
    )
    grade.create()
"""



from src.api.utils.database import db
from sqlalchemy import UniqueConstraint

class Grade(db.Model):
    __tablename__ = "grades"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'), nullable=False)
    attendance = db.Column(db.Integer, nullable=False)
    library_hours = db.Column(db.Integer, nullable=False)
    score = db.Column(db.Float(4), nullable=False)
    status = db.Column(db.String(10), nullable=False)
    session = db.Column(db.String(9), nullable=False)  
    term = db.Column(db.String(20), nullable=False)   
    school_id = db.Column(db.String(200), db.ForeignKey('admin.school_id'), nullable=False)
    is_active = db.Column(db.Boolean, default=True, nullable=False)

    __table_args__ = (
        UniqueConstraint(
            'student_id', 'course_id', 'session', 'term', 'school_id',
            name='uix_student_course_term_session_school'
        ),
    )

    def __init__(self, student_id, course_id, score, status, school_id, is_active,
                 attendance, library_hours, session, term):
        self.student_id = student_id
        self.course_id = course_id
        self.score = score
        self.status = status
        self.school_id = school_id
        self.is_active = is_active
        self.attendance = attendance
        self.library_hours = library_hours
        self.session = session
        self.term = term

    def create(self):
        db.session.add(self)
        db.session.commit()
        return self
