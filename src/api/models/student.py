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