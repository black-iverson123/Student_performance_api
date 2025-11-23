"""
Module for grade routes:
_ Create, Read, Update, Archive and Restore methods
_ Methods to handle excel file upload and template download
"""

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
from src.api.utils.access_control import permission_required
import pandas as pd
from flask import send_file
from werkzeug.utils import secure_filename
from tasks.grades import import_grades_async
from flasgger import swag_from
import io
import logging

# Setting logging
logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s")

# Creating and registering Blueprint for grade routes
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
@grade_routes.get('/download/template')
@jwt_required()
@permission_required("grades", "view")
@swag_from('../docs/grade/grade_template.yml')
def download_grade_template():
    """Download Excel template for uploading student grades"""
    try:
        # Columns for template
        template_cols = ["student_id", "course_id", "attendance", "library_hours", "score", "status", "term", 
                         "session", "school_id"]
        df = pd.DataFrame(columns=template_cols)

        # Create Excel in memory
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name="GradesTemplate")
        output.seek(0)

        return send_file(output,
            mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            download_name='grades_template.xlsx',
            as_attachment=True
        )
    except Exception as e:
        logging.debug(f"Alert {e}")
        return response_with(resp.INTERNAL_SERVER_ERROR_500, message="Failed to generate grade template.")

@grade_routes.post("/upload")
@jwt_required()
@swag_from('../docs/grade/import_grades.yml')
def import_grades():
    """
    Upload grades asynchronously
    Expects JSON list of grades
    """
    data = request.get_json()
    school_id = g.school_id  
    if not data or not isinstance(data, list):
        return response_with(resp.VALIDATION_ERROR_422, message="Grades list required.")

    # Submit Celery task
    task = import_grades_async.delay(data, school_id)

    return response_with(resp.SUCCESS_200,value={"task_id": task.id},
        message="Grades import started. Track with task ID."
    )


@grade_routes.post('/')
@jwt_required()
@swag_from('../docs/grade/grade_upload.yml')
@permission_required("grades", "upload")
def upload_grades():
    """Upload of single grade entry"""
    data = get_school_context(request.get_json())
    grade_schema = GradeSchema()

    student_id = data.get('student_id')
    course_id = data.get('course_id')
    term = data.get('term')
    session_year = data.get('session_year')

    if not all([student_id, course_id, term, session_year]):
        return response_with(resp.MISSING_PARAMETERS_422, message="Missing required fields: student_id, course_id, term, or session_year.")

    student = Student.query.filter_by(id=student_id, school_id=g.school_id).first()
    if not student:
        return response_with(resp.VALIDATION_ERROR_422, message="Student does not exist.")

    course = Course.query.filter_by(id=course_id, school_id=g.school_id).first()
    if not course:
        return response_with(resp.BAD_REQUEST_400, message="Course does not exist or does not belong to your school.")

    # Check duplicate with term + session_year
    existing = Grade.query.filter_by(
                                    student_id=student_id,
                                    course_id=course_id,
                                    school_id=g.school_id,
                                    term=term,
                                    session_year=session_year
                                ).first()
    if existing:
        return response_with(resp.CONFLICT_409, message="Grade already exists for this student, course, term & session.")

    try:
        grade = grade_schema.load(data)
        result = grade_schema.dump(grade.create())
        return response_with(resp.SUCCESS_201, value={"grade": result}, message="Grade uploaded successfully.")
    except Exception as error:
        logging.error(f"Grade Upload Error: {error}")
        return response_with(resp.BAD_REQUEST_400, message="Invalid data format or duplicate entry.")
    


@grade_routes.patch('/<int:course_id>/<int:student_id>')
@jwt_required()
@permission_required("grades", "update")
@swag_from('../docs/grade/update_grade.yml')
def update_grade(course_id, student_id):
    """Update existing grade"""
    data = get_school_context(request.get_json())

    grade = Grade.query.filter_by(
                                school_id=g.school_id,
                                course_id=course_id,
                                student_id=student_id,
                                term=data.get("term"),
                                session_year=data.get("session_year")
                            ).first()

    if not grade:
        return response_with(resp.VALIDATION_ERROR_422, message="Grade not found for this student, course, term, and session.")

    try:
        grade_schema = GradeSchema(partial=True)
        grade = grade_schema.load(data, instance=grade)
        db.session.commit()

        result = grade_schema.dump(grade)
        return response_with(resp.SUCCESS_200, value={"grade": result}, message="Grade updated successfully.")
    except Exception as error:
        logging.error(f"Grade Update Error: {error}")
        db.session.rollback()
        return response_with(resp.BAD_REQUEST_400, message="Possibly duplicate entry or invalid data.")


@grade_routes.patch('/deactivate/<int:course_id>/<int:student_id>')
@jwt_required()
@permission_required("grades", "delete")
@swag_from('../docs/grade/archive_grade.yml')
def archive_grade(course_id, student_id):
    """Archive an existing grade"""
    grade = Grade.query.filter_by(school_id=g.school_id, course_id=course_id, student_id=student_id).first_or_404()
    if not grade:
        return response_with(resp.VALIDATION_ERROR_422)
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
        return response_with(resp.INTERNAL_SERVER_ERROR_500)


@grade_routes.patch('/activate/<int:course_id>/<int:student_id>')
@jwt_required()
@permission_required("grades", "restore")
@swag_from('../docs/grade/unarchive_grade.yml')
def unarchive_grade(course_id, student_id):
    """Restore an archived grade"""
    grade = Grade.query.filter_by(school_id=g.school_id, course_id=course_id, student_id=student_id).first_or_404()
    if not grade:
        return response_with(resp.VALIDATION_ERROR_422)
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
        return response_with(resp.INTERNAL_SERVER_ERROR_500)