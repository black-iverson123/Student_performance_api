from src.api.utils.database import db
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(120), nullable=False, unique=True)
    lastname = db.Column(db.String(120), nullable=False, unique=True)
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