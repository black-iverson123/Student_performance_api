from src.api.utils.database import db
from sqlalchemy import UniqueConstraint

class Grade(db.Model):
    __tablename__ = "grades"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'), nullable=False)
    score = db.Column(db.Float(4), nullable=False)
    status = db.Column(db.String(10), nullable=False)
    school_id = db.Column(db.String(200), db.ForeignKey('admin.school_id'), nullable=False)
    is_active = db.Column(db.Boolean, default=True, nullable=False)

    __table_args__ = (
        UniqueConstraint('student_id', 'course_id', 'school_id', name='uix_school_student_course'),
    )

    def __init__(self, student_id, course_id, score, status, school_id, is_active):
        self.student_id = student_id
        self.course_id = course_id
        self.score = score
        self.status = status
        self.school_id = school_id
        self.is_active = is_active

    def create(self):
        db.session.add(self)
        db.session.commit()
        return self