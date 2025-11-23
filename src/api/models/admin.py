"""
Admin Model
===========

This module defines the `Admin` SQLAlchemy model, which represents a school administrator within the system. An Admin account is the
primary owner of a school's environment and is responsible for managing users,
students, and other school-level data.

Fields:
    id (int):
        Primary key. Auto-incrementing identifier for each admin account.

    username (str):
        Unique username for admin login.
        Required, max length ~120 characters.

    email (str):
        Unique email address for login and notifications.
        Required, max length ~120 characters.

    password (str):
        Hashed password stored using Werkzeug’s PBKDF2 hashing.
        Never stores plaintext values.

    school_name (str):
        Full name of the school associated with this admin.
        e.g., "Bright Future High School".

    school_acronym (str):
        Short, uppercase identifier for the school.
        e.g., "BFHS".

    school_id (str):
        Unique identifier automatically generated using:
            <ACRONYM>_<random 6-char hex>
        Example: "BFHS_a82f9c"
        Used to associate all students, courses, grades, and users with the school.

Relationships:
    students (relationship):
        One-to-many relationship with the Student model.
        An admin may have multiple students registered under their school.

Methods:
    __init__(username, email, password, school_name, school_acronym):
        Initializes the admin instance, hashes the password, and generates a unique school_id.

    hash_password(password):
        Static utility method that securely hashes a plaintext password.

    check_password(password):
        Compares provided plaintext password with the stored hash.

    create():
        Saves the admin instance to the database and returns it.

Business Rules:
    - Each school is uniquely identified by school_id.
    - Admin credentials (email and username) must be unique across the platform.
    - Admins manage only the data belonging to their generated school_id.

Security Notes:
    - Passwords are hashed using Werkzeug security helpers with salt.
    - Plaintext passwords are never stored or logged.

"""



from src.api.utils.database import db
from werkzeug.security import generate_password_hash, check_password_hash
import uuid


class Admin(db.Model):
    __tablename__ = "admin"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(120), nullable=False, unique=True)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password = db.Column(db.String(200), nullable=False)
    school_name = db.Column(db.String(200), nullable=False)
    school_acronym = db.Column(db.String(20), nullable=False)
    school_id = db.Column(db.String(200), nullable=False, unique=True)
    students = db.relationship('Student', backref='admin', lazy=True)
    #user = db.relationship('User', backref='admin', lazy=True)


    def __init__(self, username, email, password, school_name, school_acronym):
        self.username = username
        self.email = email
        self.password = self.hash_password(password)
        self.school_name = school_name
        self.school_acronym = school_acronym
        self.school_id = f"{school_acronym.upper()}_{str(uuid.uuid4().hex[:6])}"

    
    @staticmethod
    def hash_password(password):
        return generate_password_hash(password, salt_length=12)
    
    def check_password(self, password):
        return check_password_hash(self.password, password)

    def create(self):
        db.session.add(self)
        db.session.commit()
        return self


