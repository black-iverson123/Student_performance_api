from flask import Blueprint, request, g
from src.api.utils.database import db
from src.api.models.student import Student
from src.api.schema.student_schema import StudentSchema
from src.api.utils.responses import response_with
from src.api.utils import responses as resp
from flask_jwt_extended import jwt_required,get_jwt, get_jwt_identity
import logging

logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s")

student_routes = Blueprint("student_routes", __name__)  

# context handler
@student_routes.before_request
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
        logging.debug(f"Alert: JWT context not set: {e}")
@student_routes.post('/')
@jwt_required()
def create_student():
    data = request.get_json()
    data["school_id"] = g.school_id

    student_schema = StudentSchema()
    student = student_schema.load(data)

    try:
        result = student_schema.dump(student.create())
        return response_with(
            resp.SUCCESS_201,
            value={"student": result},
            message=f"You've successfully added {student.firstname}"
        )
    except Exception as error:
        logging.debug(f"Alert: {str(error)}")
        return response_with(resp.INVALID_INPUT_422)

# remember to apply pagination
@student_routes.get('/')
@jwt_required()
def get_students():
    students = Student.query.filter_by(school_id=g.school_id).all()
    student_schema =StudentSchema(many=True)
    data = student_schema.dump(students)
    return response_with(resp.SUCCESS_200, value={'students': data})

@student_routes.get('/<int:student_id>')
@jwt_required()
def get_student_by_id(student_id):
    student  = Student.query.filter_by(school_id=g.school_id, id=student_id).first()

    if student is None:
        return response_with(resp.INVALID_INPUT_422)
    try:
        student_schema  = StudentSchema()
        data = student_schema.dump(student)
        return response_with(resp.SUCCESS_200, value={'student': data})
    except Exception as error:
        logging.debug(f"Alert: {str(error)}")
        return response_with(resp.SERVER_ERROR_500)

@student_routes.patch('/<int:student_id>')
@jwt_required()
def update_student(student_id):
    data = request.get_json()
    student = Student.query.filter_by(school_id=g.school_id, id=student_id).first()
    if student is None:
        return response_with(resp.INVALID_INPUT_422)
    try:
        student_schema = StudentSchema(partial=True)
        student = student_schema.load(data, instance=student)
        db.session.commit()
        result = student_schema.dump(student)
        return response_with(resp.SUCCESS_200, value={"student": result}, message=f"You've successfully updated {student.firstname}")
    except Exception as error:
        logging.debug(f"Alert: {str(error)}")
        db.session.rollback()
        return response_with(resp.SERVER_ERROR_500)

@student_routes.patch('/deactivate/<int:student_id>')
@jwt_required()
def archive_students(student_id):
    student = Student.query.filter_by(school_id=g.school_id, id=student_id).first()
    if not student:
        return response_with(resp.INVALID_INPUT_422)
    try:
        student.is_active = False
        db.session.commit()
        student_schema = StudentSchema()
        result = student_schema.dump(student)
        return response_with(resp.SUCCESS_200, value={"student": result}, message=f"Student {student.firstname} has been archived")
    except Exception as error:
        logging.debug(f"Alert: {error}")
        db.session.rollback()
        return response_with(resp.SERVER_ERROR_500)

@student_routes.patch('/activate/<int:student_id>')
@jwt_required()
def unarchive_students(student_id):
    student = Student.query.filter_by(school_id=g.school_id, id=student_id).first()
    if not student:
        return response_with(resp.INVALID_INPUT_422)
    try:
        student.is_active = True
        db.session.commit()
        student_schema = StudentSchema()
        result = student_schema.dump(student)
        return response_with(resp.SUCCESS_200, value={"student": result}, message=f"Student {student.firstname} has been unarchived")
    except Exception as error:
        logging.debug(f"Alert: {error}")
        db.session.rollback()
        return response_with(resp.SERVER_ERROR_500)