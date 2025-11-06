# 🏫 Student Management API

A **Flask-based RESTful API** for managing students, schools, and administrators.  
This project supports secure authentication via JWT, and role-based data access where each admin manages only their own school’s students.

---

## 🚀 Features

- 🔐 **JWT Authentication** (Admin login + protected routes)
- 🧑‍🏫 **Admin Management**
  - Create and authenticate admins
  - Automatically assign unique `school_id` and `school_acronym`
- 🎓 **Student Management**
  - Create, update, retrieve, and deactivate students
  - Students are automatically tied to an admin’s `school_id`
- 🧾 **Grades (Optional Extension)**
  - Store and query academic performance
- ⚙️ **Context-Aware API**
  - Automatically loads `school_id` and `user_email` from JWT into Flask’s global context (`g`)
- 🧪 **Unit & Integration Tests**
  - Powered by `unittest` and Flask’s test client
  - Includes full CRUD coverage for admin and student routes

---

## 🏗️ Project Structure

├── aew
├── main.py
├── migrations
│   ├── alembic.ini
│   ├── env.py
│   ├── __pycache__
│   ├── README
│   ├── script.py.mako
│   └── versions
├── myenv
│   ├── bin
│   ├── include
│   ├── lib
│   ├── lib64 -> lib
│   └── pyvenv.cfg
├── __pycache__
│   ├── main.cpython-312.pyc
│   └── run.cpython-312.pyc
├── readme.md
├── requirements.txt
├── run.py
├── seeder.py
├── src
│   ├── api
│   ├── __init__.py
│   ├── __pycache__
│   ├── static
│   └── templates
└── tests
    ├── __pycache__
    ├── test_admin.py
    ├── test_base.py
    ├── test_course.py
    └── test_student.py


---

## ⚙️ Installation & Setup

### 1️⃣ Clone the repository

```bash
git clone https://github.com/black-iverson123/student-management-api.git
cd student-management-api

## Create a virtual environment
python -m venv venv
source venv/bin/activate   # On Windows use: venv\Scripts\activate

## Install Dependencies
pip install -r requirements.txt


## create a .env file at root
FLASK_ENV=development
SECRET_KEY=your_secret_key
JWT_SECRET_KEY=your_jwt_secret
SQLALCHEMY_DATABASE_URI=sqlite:///students.db or mysql uri


## Run
 
python3 run.py

## To runtests
# All tests create an instance SQLite database
python -m unittest discover -s tests


🧰 Technologies Used

Flask — Web framework

Flask-JWT-Extended — Authentication

SQLAlchemy — ORM

Marshmallow — Serialization

SQLite / PostgreSQL — Database

Unittest — Testing framework


👩‍💻 Author

Adebowale Obalanlege
Backend & Data Developer | Flask • Cloud • SQL • Data Science
📧 maxwelladebowale6@gmail.com
