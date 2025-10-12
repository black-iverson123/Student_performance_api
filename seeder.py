from faker import Faker
import random
from src.api.utils.database import db
from src.api.models.student import Student
from src.api.models.course import Course
from src.api.models.grade import Grade
from main import app

fake = Faker()

def create_courses(n):
    """Create a random number of courses if they don't already exist."""
    existing_courses = Course.query.count()
    if existing_courses >= n:
        print(f"Alert: Found {existing_courses} courses, skipping course seeding.")
        return Course.query.all()

    courses = []
    for _ in range(n):
        title = fake.word().capitalize() + " " + random.choice(["101", "202", "303", "404"])
        code = title.split()[0][:3].upper() + str(random.randint(100, 499))
        passing_grade = random.randint(50, 75)

        if Course.query.filter_by(course_code=code).first():
            continue  

        course = Course(course_title=title, course_code=code, passing_grade=passing_grade)
        db.session.add(course)
        courses.append(course)

    db.session.commit()
    print(f"Info: Created {len(courses)} new courses.")
    return Course.query.all()


def create_students(n):
    """Create a random number of students if they don't already exist."""
    existing_students = Student.query.count()
    if existing_students >= n:
        print(f"Alert: Found {existing_students} students, skipping student seeding.")
        return Student.query.all()

    students = []
    for _ in range(n):
        firstname = fake.first_name()
        lastname = fake.last_name()
        email = f"{firstname.lower()}.{lastname.lower()}@example.com"

        if Student.query.filter_by(email=email).first():
            continue  

        student = Student(firstname=firstname, lastname=lastname, email=email)
        db.session.add(student)
        students.append(student)

    db.session.commit()
    print(f"Info: Created {len(students)} new students.")
    return Student.query.all()


def create_grades(students, courses):
    """Assign random grades to existing students for existing courses."""
    total_before = Grade.query.count()

    for student in students:
        num_courses = random.randint(2, len(courses))
        sampled_courses = random.sample(courses, num_courses)
        for course in sampled_courses:
            existing = Grade.query.filter_by(student_id=student.id, course_id=course.id).first()
            if existing:
                continue

            score = random.uniform(0, 100)
            status = "Passed" if score >= course.passing_grade else "Failed"
            grade = Grade(
                student_id=student.id,
                course_id=course.id,
                score=score,
                status=status
            )
            db.session.add(grade)

    db.session.commit()
    total_after = Grade.query.count()
    print(f"Info: Created {total_after - total_before} new grades.")


def seed_all():
    with app.app_context():
        print("Seeding data...")
        courses = create_courses(20)
        students = create_students(100)
        create_grades(students, courses)
        print("Date seeding completed successfully!")


if __name__ == "__main__":
    seed_all()
