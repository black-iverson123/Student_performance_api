"""
Student Model
=============

This module defines the `Student` SQLAlchemy model, which represents individual 
students enrolled within a particular school. It stores basic student identity 
information and establishes relationships with grade records.

Model Purpose:
    - Represent students in the database.
    - Store essential personal and academic identification fields.
    - Associate students with their respective schools.
    - Link students to all of their grade records through a one-to-many relationship.

Table Name:
    student

Fields:
    id (Integer, PK):
        Auto-incrementing primary identifier for each student.

    firstname (String(120), required):
        Student's first name.

    lastname (String(120), required):
        Student's last name.

    email (String(120), unique, required):
        Used for student identification and optional notifications.
        Uniqueness ensures no duplicate student accounts.

    grades (relationship -> Grade):
        One-to-many relationship linking a student to all their grade entries.

    school_id (String(200), FK -> admin.school_id):
        Ensures that students are scoped to the school that created them.
        Enables multi-tenancy.

    is_active (Boolean, default=True):
        Marks whether the student is active or archived/deleted.

Methods:
    __init__(firstname, lastname, email, school_id, is_active):
        Initializes the Student instance with required attributes.

    create():
        Saves the student record into the database and commits the transaction.

Usage Example:
    student = Student(
        firstname="John",
        lastname="Doe",
        email="john.doe@example.com",
        school_id="SCH_ABC123",
        is_active=True
    )
    student.create()
"""



from src.api.utils.database import db

class Student(db.Model):
    __tablename__ = "student"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    firstname = db.Column(db.String(120), nullable=False)
    lastname = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    grades = db.relationship('Grade', backref="student", lazy=True)
    school_id = db.Column(db.String(200), db.ForeignKey('admin.school_id'), nullable=False)
    is_active = db.Column(db.Boolean, default=True, nullable=False)

    def __init__(self, firstname, lastname, email, school_id, is_active):
        self.firstname = firstname
        self.lastname = lastname
        self.email = email
        self.school_id = school_id
        self.is_active = is_active
        
    
    def create(self):
        db.session.add(self)
        db.session.commit()
        return self