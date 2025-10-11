from api.utils.database import db

class Student(db.Model):
    __tablename__ = "student"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    firstname = db.Column(db.String(120), nullable=False)
    lastname = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    grades = db.relationship('Grade', backref="student", lazy=True)

    def __init__(self, firstname, lastname, email, grades):
        self.lastname = lastname
        self.lastname = lastname
        self.email = email
        #self.grades = grades
    
    def create(self):
        db.session.add(self)
        db.session.commit()
        return self