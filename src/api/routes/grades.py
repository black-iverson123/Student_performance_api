from flask import Blueprint, request, g
from src.api.utils.database import db
from src.api.models.course import Course
from src.api.models.grade import Grade
from src.api.models.student import Student
from src.api.schema.grade_schema import GradeSchema
from src.api.utils.responses import response_with
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from src.api.utils import responses as resp
from src.api.utils.helper import get_school_context
import logging

logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s")

grade_routes = Blueprint("grade_routes", __name__)  

# context handler
@grade_routes.before_request
@jwt_required()
def load_jwt_context():
    """
    Automatically loads school_id and user_email from the JWT into Flask's global context (g)
    for every request that includes a valid JWT. If no JWT is provided, g remains empty.
    """
    try:
        claims = get_jwt()
        identity = get_jwt_identity()

        if claims:
            g.school_id = claims.get('school_id')
        else:
            g.school_id = None

        g.user_email = identity
    except Exception as e:
        # Handles routes where JWT isn't required or is missing
        g.school_id = None
        g.user_email = None
        logging.debug(f"JWT context not set: {e}")


#ROUTES

@grade_routes.post('/')
@jwt_required()
def upload_grades():
    data = get_school_context(request.get_json())
    grade_schema = GradeSchema()
    
    #validate course belong to same school
    course_id = data.get('course_id')
    student_id = data.get('student_id')
    course = Course.query.filter_by(id=course_id, school_id=g.school_id).first()
    student = Student.query.filter_by(id=student_id, school_id=g.school_id).first()
    if not student:
        return response_with(resp.INVALID_INPUT_422, message="Student does not exist.")
    
    if not course:
         return response_with(resp.INVALID_INPUT_422, message="Course does not exist or does not belong to your school.")
    try:
        grade = grade_schema.load(data)
        result = grade_schema.dump(grade.create())
        return response_with(resp.SUCCESS_201, value={"grade": result}, message="Grade uploaded successfully.")
    except Exception as error:
        logging.debug(f"Alert: {str(error)}")
        return response_with(resp.INVALID_INPUT_422, message=f"Invalid data (possible duplicate entry)")

@grade_routes.patch('/<int:course_id>/<int:student_id>')
@jwt_required()
def update_grade(course_id, student_id):
    data = request.get_json()
    grade = Grade.query.filter_by(school_id=g.school_id, course_id=course_id, student_id=student_id).first_or_404()
    if not grade:
        return response_with(resp.INVALID_INPUT_422)
    student = Student.query.filter_by(id=student_id, school_id=g.school_id).first()
    try:
        grade_schema = GradeSchema(partial=True)
        grade = grade_schema.load(data, instance=grade)
        db.session.commit()
        result = grade_schema.dump(grade)
        return response_with(resp.SUCCESS_200, value={"grade": result}, message=f"Grade updated successfully for {student.firstname}.")
    except Exception as error:
        logging.debug(f"Alert: {error}")
        db.session.rollback()
        return response_with(resp.INVALID_INPUT_422, message="Possibe duplicate entry or invalid data.")

@grade_routes.patch('/deactivate/<int:course_id>/<int:student_id>')
@jwt_required()
def archive_grade(course_id, student_id):
    grade = Grade.query.filter_by(school_id=g.school_id, course_id=course_id, student_id=student_id).first_or_404()
    if not grade:
        return response_with(resp.INVALID_INPUT_422)
    student = Student.query.filter_by(id=student_id, school_id=g.school_id).first()
    try:
        grade.is_active = False
        db.session.commit()
        grade_schema = GradeSchema()
        result = grade_schema.dump(grade)
        return response_with(resp.SUCCESS_200, value={"grade": result}, message=f"Grade archived successfully for {student.firstname}.")
    except Exception as error:
        logging.debug(f"Alert: {error}")
        db.session.rollback()
        return response_with(resp.SERVER_ERROR_500)


@grade_routes.patch('/activate/<int:course_id>/<int:student_id>')
@jwt_required()
def unarchive_grade(course_id, student_id):
    grade = Grade.query.filter_by(school_id=g.school_id, course_id=course_id, student_id=student_id).first_or_404()
    if not grade:
        return response_with(resp.INVALID_INPUT_422)
    student = Student.query.filter_by(id=student_id).first()
    try:
        grade.is_active = True
        db.session.commit()
        grade_schema = GradeSchema()
        result = grade_schema.dump(grade)
        return response_with(resp.SUCCESS_200, value={"grade": result}, message=f"Grade archived successfully for {student.firstname}.")
    except Exception as error:
        logging.debug(f"Alert: {error}")
        db.session.rollback()
        return response_with(resp.SERVER_ERROR_500)