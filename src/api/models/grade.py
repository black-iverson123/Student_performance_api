from src.api.utils.database import db


class Grade(db.Model):
    __tablename__ = "grades"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=True)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'), nullable=True)
    score = db.Column(db.Float(4), nullable=False)
    status = db.Column(db.String(10), nullable=False)

    def __init__(self, student_id, course_id, score, status):
        self.student_id = student_id
        self.course_id = course_id
        self.score = score
        self.status = status

    def create(self):
        db.session.add(self)
        db.session.commit()
        return self