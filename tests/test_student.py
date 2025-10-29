import json
from test_base import BaseTestCase
from src.api.models.admin import Admin
from src.api.models.student import Student

class TestStudentRoute(BaseTestCase):
    def setUp(self):
        super().setUp()

        # Create admin
        self.admin = Admin(
            username="Admin2",
            email="Admin2@example.com",
            password="12345",
            school_name="Jujutsu High",
            school_acronym="JJK"
        ).create()

        #Create student
        self.student = Student(
            firstname="Tenten",
            lastname="Higurashi",
            email="tenten@example.com",
            school_id=self.admin.school_id,
            is_active=True
        ).create()


        # Login to get access token
        login_payload = {
            "email": "Admin2@example.com",
            "password": "12345"
        }

        login_response = self.client.post(
            "/api/admin/login",
            data=json.dumps(login_payload),
            content_type="application/json"
        )

        self.assertEqual(login_response.status_code, 200)
        tokens = json.loads(login_response.data)
        self.access_token = tokens["access_token"]

    def test_create_student(self):
        """Test creating a student via POST /api/students with valid token"""

        payload = {
            "firstname": "Kise",
            "lastname": "Ryota",
            "email": "kise@example.com"
        }

        response = self.client.post(
            "/api/students/",
            data=json.dumps(payload),
            headers={
                "Authorization": f"Bearer {self.access_token}",
                "Content-Type": "application/json"
            }
        )

        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        self.assertIn("student", data)
        self.assertEqual(data["student"]["email"], "kise@example.com")

    def test_create_student_without_token(self):
        """Test creating student without JWT via POST /api/students"""

        payload = {
            "firstname": "Aomine",
            "lastname": "Daiki",
            "email": "aomine@example.com"
        }

        response = self.client.post(
            "/api/students/",
            data=json.dumps(payload),headers={
            "Authorization": None,
            "Content-Type": "application/json"}
        )

        # This line is expected to fail no token for route
        self.assertEqual(response.status_code, 401)
    
    def test_get_student(self):
        """Testing endpoint via GET /api/students"""

        response = self.client.get("/api/students/", headers={
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json"
        })

        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertIn("students", data)
    
    def test_get_student_no_token(self):
        """Testing endpoint via GET /api/students no token"""

        response = self.client.get("/api/students/", headers={
            "Authorization": None,
            "Content-Type": "application/json"
        })

        data = json.loads(response.data)

       # This line is expected to fail no token for route
        self.assertEqual(response.status_code, 401)
    
    def test_get_student_id(self):
        """Testing endpoint via GET /api/students/<int: student_id>"""

        payload = {
            "student_id": 1
        }

        response = self.client.get(f"/api/students/{payload['student_id']}",
                                   headers={
                                       "Authorization": f"Bearer {self.access_token}",
                                       "content-type": "application/json"
                                   })

        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertIn("student", data)
    
    def test_get_student_id_no_token(self):
        """Testing endpoint via GET /api/students/<int: student_id>"""

        payload = {
            "student_id": 1
        }

        response = self.client.get(f"/api/students/{payload['student_id']}",
                                   headers={
                                       "Authorization": None,
                                       "content-type": "application/json"
                                   })

        data = json.loads(response.data)

       # This line is expected to fail no token for route
        self.assertEqual(response.status_code, 401)
    
    def test_update_student(self):
        """Testing endpoint via PATCH /api/students/<int: student_id>"""

        student_id = 1 
        payload = {
            "lastname": "Hyuuga"
        }

        response = self.client.patch(f'/api/students/{student_id}', data=json.dumps(payload),
                                     headers={"Authorization": f"Bearer {self.access_token}",
                                              "content-type": "application/json"
        })
        
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 200)
        self.assertIn("student", data)
    
    def test_update_student_no_token(self):
        """Testing endpoint via PATCH /api/students/<int: student_id>"""

        student_id = 1 
        payload = {
            "lastname": "Hyuuga"
        }

        response = self.client.patch(f'/api/students/{student_id}', data=json.dumps(payload),
                                     headers={"Authorization": None,
                                              "content-type": "application/json"
        })
        
        data = json.loads(response.data)
        
       # This line is expected to fail no token for route
        self.assertEqual(response.status_code, 401)
    
    def test_archive_student(self):
        """Testing endpoint via PATCH /api/students/deactivate/<int: student_id>"""
        student_id = 1
        
        response = self.client.patch(f"/api/students/deactivate/{student_id}",
                                     headers={"Authorization": f"Bearer {self.access_token}",
                                              "content-type": "application/json"})
        
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertIn("student", data)
    
    def test_archive_student_no_token(self):
        """Testing endpoint via PATCH /api/students/deactivate/<int: student_id>"""
        student_id = 1
        
        response = self.client.patch(f"/api/students/deactivate/{student_id}",
                                     headers={"Authorization": None,
                                              "content-type": "application/json"})
        
        data = json.loads(response.data)

        # This line is expected to fail no token for route
        self.assertEqual(response.status_code, 401)
    
    def test_unarchive_student(self):
        """Testing endpoint via PATCH /api/students/activate/<int: student_id>"""
        student_id = 1

        response = self.client.patch(f"/api/students/activate/{student_id}",
                                     headers={"Authorization": f"Bearer {self.access_token}",
                                              "content-type": "application/json"})
        
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertIn("student", data)
    
    def test_unarchive_student_no_token(self):
        """Testing endpoint via PATCH /api/students/activate/<int: student_id>"""
        student_id = 1

        response = self.client.patch(f"/api/students/activate/{student_id}",
                                     headers={"Authorization": None,
                                              "content-type": "application/json"})
        
        data = json.loads(response.data)

        # This line is expected to fail no token for route
        self.assertEqual(response.status_code, 401)


        
 


