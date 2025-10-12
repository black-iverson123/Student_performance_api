from flask import Blueprint, request
from src.api.utils.database import db
from src.api.models.course import Course
from src.api.schema.course_schema import CourseSchema
from src.api.utils.responses import response_with
from src.api.utils import responses as resp
import logging

logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s")


course_routes = Blueprint("course_routes", __name__)


@course_routes.post('/')
def create_course():
    data = request.get_json()
    course_schema = CourseSchema()
    course = course_schema.load(data)
    try:
        result = course_schema.dump(course.create())
        return response_with(resp.SUCCESS_201, value={"course": result})
    except Exception as e:
        logging.debug(f"Alert: {str(e)}")
        return response_with(resp.INVALID_INPUT_422)

@course_routes.get('/')
def get_courses():
    courses = Course.query.all()
    course_schema = CourseSchema(many=True, only=['course_code', 'course_title', 'passing_grade'])
    data = course_schema.dump(courses)
    return response_with(resp.SUCCESS_200, value={'courses': data})

@course_routes.get('/<course_code>')
def get_course(course_code):
    course = Course.query.filter_by(course_code=course_code).first()
    if course is None:
        return response_with(resp.INVALID_INPUT_422)
    try:
        course_schema = CourseSchema()
        data = course_schema.dump(course)
        return response_with(resp.SUCCESS_200, value={'course': data})
    except Exception as e:
        logging.debug(f"Alert: {str(e)}")
        return response_with(resp.SERVER_ERROR_500)

@course_routes.patch('/<course_code>')
def update_course(course_code):
    data = request.get_json()
    course = Course.query.filter_by(course_code=course_code).first()
    if course is None:
        return response_with(resp.INVALID_INPUT_422)
    try:
        course_schema = CourseSchema(partial=True)
        course = course_schema.load(data, instance=course)
        db.session.commit()
        result = course_schema.dump(course)
        return response_with(resp.SUCCESS_200, value={"course": result})
    except Exception as e:
        logging.debug(f"Alert: {str(e)}")
        db.session.rollback()
        return response_with(resp.SERVER_ERROR_500)

@course_routes.delete('/<course_code>')
def delete_course(course_code):
    course = Course.query.filter_by(course_code=course_code).first()
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
