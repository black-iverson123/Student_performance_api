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