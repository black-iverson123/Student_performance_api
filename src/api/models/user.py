
"""
User Model
==========

This module defines the `User` SQLAlchemy model, representing system users 
(teachers, staff, or school admins) associated with a particular school.  
It handles authentication (password hashing), authorization (roles), and 
associates each user with their parent admin account.

Model Purpose:
    - Provide user accounts for teachers or school staff.
    - Support authentication through secure password hashing.
    - Associate users with a specific school and the admin who created them.
    - Store user roles for permission-based access.

Table Name:
    user

Fields:
    id (Integer, PK):
        Unique identifier for each user.

    firstname (String(120), required):
        User's first name.

    lastname (String(120), required):
        User's last name.

    email (String(120), unique, required):
        Primary login identifier. Ensures no duplicate accounts.

    password (String(250), required):
        Securely hashed password using Werkzeug. Plaintext is never stored.

    role (String(50), default='teacher'):
        Defines user privileges (e.g., 'teacher', 'staff', 'manager').

    school_id (String(200), FK -> admin.school_id):
        Ensures users belong to a specific school for multi-tenancy.

    admin_id (Integer, FK -> admin.id):
        References the admin who created this user account.

    admin (relationship -> Admin):
        Establishes an ORM relationship to the Admin entity.

    is_active (Boolean, default=True):
        Allows soft deletion / account deactivation.

Methods:
    __init__(firstname, lastname, email, password, role, school_id, admin_id, is_active):
        Initializes the User instance and automatically hashes the password.

    hash_password(password):
        Static method. Returns a hashed version of the password.

    check_password(password):
        Verifies a password against the stored hash.

    create():
        Saves the user record in the database and commits the transaction.

Usage Example:
    user = User(
        firstname="Jane",
        lastname="Doe",
        email="jane@example.com",
        password="securepass123",
        role="teacher",
        school_id="SCH_ABC123",
        admin_id=1,
        is_active=True
    )
    user.create()
"""

from src.api.utils.database import db
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(120), nullable=False)
    lastname = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(250), nullable=False)
    role = db.Column(db.String(50), default='teacher')
    school_id = db.Column(db.String(200), db.ForeignKey('admin.school_id'), nullable=False)
    admin_id = db.Column(db.Integer, db.ForeignKey('admin.id'))
    admin = db.relationship('Admin', backref='user', lazy=True, foreign_keys=[admin_id]) #specifying which FK to use
    is_active = db.Column(db.Boolean, default=True, nullable=False)

    def __init__(self, firstname, lastname, email, password, role,  school_id, admin_id, is_active):
        self.firstname = firstname
        self.lastname= lastname
        self.email = email
        self.password = self.hash_password(password)
        self.role = role
        self.school_id = school_id
        self.admin_id = admin_id
        self.is_active = is_active

    
    @staticmethod
    def hash_password(password):
        return generate_password_hash(password, salt_length=12)
    
    def check_password(self, password):
        return check_password_hash(self.password, password)
    
    def create(self):
        db.session.add(self)
        db.session.commit()
        return self