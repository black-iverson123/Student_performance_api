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


