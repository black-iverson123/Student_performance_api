from flask import Blueprint, request, g
from src.api.utils.database import db
from src.api.models.course import Course
from src.api.schema.course_schema import CourseSchema
from src.api.utils.responses import response_with
from src.api.utils import responses as resp
from src.api.utils.helper import get_school_context
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
import logging

logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s")

course_routes = Blueprint("course_routes", __name__)

# context handler
@course_routes.before_request
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

# ROUTES
@course_routes.post('/')
@jwt_required()
def create_course():
    data = get_school_context(request.get_json())
    course_schema = CourseSchema()
    course = course_schema.load(data)
    try:
        result = course_schema.dump(course.create())
        return response_with(resp.SUCCESS_201, value={"course": result})
    except Exception as error:
        logging.debug(f"Alert: {str(error)}")
        return response_with(resp.INVALID_INPUT_422)


@course_routes.get('/')
@jwt_required()
def get_courses():
    courses = Course.query.filter_by(school_id=g.school_id).all()
    course_schema = CourseSchema(many=True, only=['course_code', 'course_title', 'passing_grade'])
    data = course_schema.dump(courses)
    return response_with(resp.SUCCESS_200, value={'courses': data})


@course_routes.get('/<course_code>')
@jwt_required()
def get_course_by_code(course_code):
    course = Course.query.filter_by(course_code=course_code, school_id=g.school_id).first()
    if course is None:
        return response_with(resp.INVALID_INPUT_422)
    try:
        course_schema = CourseSchema()
        data = course_schema.dump(course)
        return response_with(resp.SUCCESS_200, value={'course': data})
    except Exception as error:
        logging.debug(f"Alert: {str(error)}")
        return response_with(resp.SERVER_ERROR_500)


@course_routes.patch('/<course_code>')
@jwt_required()
def update_course(course_code):
    allowed_changes = ['course_title', 'passing_grade']
    data = get_school_context(request.get_json(), creator=False)

    # Enforce allowed changes
    for key in data.keys():
        if key not in allowed_changes:
            return response_with(resp.INVALID_INPUT_422, message=f"Field '{key}' cannot be updated.")
        
    course = Course.query.filter_by(course_code=course_code, school_id=g.school_id).first()
    if course is None:
        return response_with(resp.INVALID_INPUT_422)

    try:
        course_schema = CourseSchema(partial=True)
        course = course_schema.load(data, instance=course)
        db.session.commit()
        result = course_schema.dump(course)
        return response_with(resp.SUCCESS_200, value={"course": result})
    except Exception as error:
        logging.debug(f"Alert: {str(error)}")
        db.session.rollback()
        return response_with(resp.SERVER_ERROR_500)


@course_routes.delete('/<course_code>')
@jwt_required()
def delete_course(course_code):
    course = Course.query.filter_by(course_code=course_code, school_id=g.school_id).first()
    if course is None:
        return response_with(resp.INVALID_INPUT_422)
    try:
        course_title = course.course_title
        db.session.delete(course)
        db.session.commit()
        return response_with(resp.SUCCESS_202, message=f"You have successfully deleted {course_title}")
    except Exception as error:
        logging.debug(f"Alert {error}")
        db.session.rollback()
        return response_with(resp.SERVER_ERROR_500)
