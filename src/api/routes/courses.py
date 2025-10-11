from flask import Blueprint
from api.utils.database import db
from api.models.course import Course


course_routes = Blueprint("course_routes", __name__)


@course_routes.post('/')
