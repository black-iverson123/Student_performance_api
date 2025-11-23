"""
Module for student routes:
_ Create, Read, Update, Archive and Restore methods
"""


from flask import Blueprint, request, g
from src.api.utils.database import db
from src.api.models.student import Student
from src.api.schema.student_schema import StudentSchema
from src.api.utils.responses import response_with
from src.api.utils import responses as resp
from src.api.utils.access_control import permission_required
from flask_jwt_extended import jwt_required,get_jwt, get_jwt_identity
from flasgger import swag_from
import logging


#setting logging
logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s")

# Creating and registering Blueprint for student_routes
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


#Routes
@student_routes.post('/')
@jwt_required()
@permission_required("students", "create")
@swag_from('../docs/student/create_student.yml')
def create_student():
    """Create a new student"""
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
        return response_with(resp.BAD_REQUEST_400)

# remember to apply pagination
@student_routes.get('/')
@jwt_required()
@permission_required("students", "get_all")
@swag_from('../docs/student/get_students.yml')
def get_students():
    """Retrieve all students with pagination"""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    pagination = Student.query.filter_by(school_id=g.school_id).paginate(page=page, per_page=per_page, error_out=False)
    students = pagination.items
    student_schema =StudentSchema(many=True)
    data = student_schema.dump(students)
    return response_with(resp.SUCCESS_200, 
                         value={'students': data},
                         pagination={
                                'total': pagination.total,
                                'page': pagination.page,
                                'per_page': pagination.per_page,
                                'pages': pagination.pages
                         }
                        )

@student_routes.get('/<int:student_id>')
@jwt_required()
@permission_required("students", "get_one")
@swag_from('../docs/student/get_student.yml')
def get_student_by_id(student_id):
    """Retrieve a single student by ID"""
    student  = Student.query.filter_by(school_id=g.school_id, id=student_id).first()

    if student is None:
        return response_with(resp.VALIDATION_ERROR_422)
    try:
        student_schema  = StudentSchema()
        data = student_schema.dump(student)
        return response_with(resp.SUCCESS_200, value={'student': data})
    except Exception as error:
        logging.debug(f"Alert: {str(error)}")
        return response_with(resp.INTERNAL_SERVER_ERROR_500)

@student_routes.patch('/<int:student_id>')
@jwt_required()
@permission_required("students", "update")
@swag_from('../docs/student/update_student.yml')
def update_student(student_id):
    """Update a existing student detail"""
    data = request.get_json()
    student = Student.query.filter_by(school_id=g.school_id, id=student_id).first()
    if student is None:
        return response_with(resp.VALIDATION_ERROR_422)
    try:
        student_schema = StudentSchema(partial=True)
        student = student_schema.load(data, instance=student)
        db.session.commit()
        result = student_schema.dump(student)
        return response_with(resp.SUCCESS_200, value={"student": result}, message=f"You've successfully updated {student.firstname}")
    except Exception as error:
        logging.debug(f"Alert: {str(error)}")
        db.session.rollback()
        return response_with(resp.INTERNAL_SERVER_ERROR_500)

@student_routes.patch('/deactivate/<int:student_id>')
@jwt_required()
@permission_required("students", "delete")
@swag_from('../docs/student/archive_student.yml')
def archive_students(student_id):
    """Archive a student"""
    student = Student.query.filter_by(school_id=g.school_id, id=student_id).first()
    if not student:
        return response_with(resp.VALIDATION_ERROR_422)
    try:
        student.is_active = False
        db.session.commit()
        student_schema = StudentSchema()
        result = student_schema.dump(student)
        return response_with(resp.SUCCESS_200, value={"student": result}, message=f"Student {student.firstname} has been archived")
    except Exception as error:
        logging.debug(f"Alert: {error}")
        db.session.rollback()
        return response_with(resp.INTERNAL_SERVER_ERROR_500)

@student_routes.patch('/activate/<int:student_id>')
@jwt_required()
@permission_required("students", "restore")
@swag_from('../docs/student/unarchive_student.yml')
def unarchive_students(student_id):
    """Restore an archived student"""
    student = Student.query.filter_by(school_id=g.school_id, id=student_id).first()
    if not student:
        return response_with(resp.VALIDATION_ERROR_422)
    try:
        student.is_active = True
        db.session.commit()
        student_schema = StudentSchema()
        result = student_schema.dump(student)
        return response_with(resp.SUCCESS_200, value={"student": result}, message=f"Student {student.firstname} has been unarchived")
    except Exception as error:
        logging.debug(f"Alert: {error}")
        db.session.rollback()
        return response_with(resp.INTERNAL_SERVER_ERROR_500)