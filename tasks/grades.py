"""
Asynchronous task module for importing student grades.

This module defines a Celery task to handle the bulk import of grades
into the database asynchronously. Using Celery ensures that large 
grade imports do not block the main Flask application.

Modules:
    - celery_worker: Provides the configured Celery instance.
    - src.api.models.grade: SQLAlchemy Grade model for database operations.
    - src.api.utils.database: SQLAlchemy database session.
    - logging: Python logging module for task tracking.

Functions:
    import_grades_async: Celery task that inserts multiple grades for a school.
        Parameters:
            - grades_list (list[dict]): Each dict should contain:
                * student_id: int
                * course_id: int
                * score: float
                * attendance: int
                * library_hours: int
                * status: str ('Passed' or 'Failed')
                * session: str (e.g., "2024/2025")
                * term: str (e.g., "First Term")
            - school_id (str): Identifier for the school to associate grades with.
        Returns:
            dict: Summary of the import operation, e.g., {"imported": 10}
"""


from celery_worker import celery
from src.api.models.grade import Grade
from src.api.utils.database import db
import logging

@celery.task(bind=True)
def import_grades_async(self, grades_list, school_id):
    """
    Asynchronously import a list of grades.
    grades_list: list of dicts containing:
      - student_id
      - course_id
      - score
      - attendance
      - library_hours
      - status
    """
    created_count = 0
    for data in grades_list:
        # Check for existing grade
        existing = Grade.query.filter_by(
                                            student_id=data['student_id'], 
                                            course_id=data['course_id'],
                                            school_id=school_id
                                        ).first()
        if existing:
            continue

        grade = Grade(
                        student_id=data['student_id'],
                        course_id=data['course_id'],
                        score=data['score'],
                        attendance=data['attendance'],
                        library_hours=data['library_hours'],
                        status=data['status'],
                        school_id=school_id,
                        is_active=True,
                        session=data['session'],
                        term=data['term']
                    )
        db.session.add(grade)
        created_count += 1

    db.session.commit()
    logging.info(f"Imported {created_count} grades for school {school_id}.")
    return {"imported": created_count}
