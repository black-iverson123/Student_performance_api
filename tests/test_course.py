import json
from test_base import BaseTestCase
from src.api.models.admin import Admin
from src.api.models.course import Course


class TestCourseRoute(BaseTestCase):
    def setUp(self):
        super().setUp()

        #create admin
        self.admin = Admin(
            username="Admin2",
            email="Admin2@example.com",
            password="12345",
            school_name="Jujutsu High",
            school_acronym="JJK"
        ).create()

        #Create course
        self.course = Course(
            course_title="Ninja tactics",
            course_code="NNT101",
            passing_grade=85,
            school_id=self.admin.school_id
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
    
    def test_create_course(self):
        """Testing creating a course via POST /api/courses/"""

        payload = {
            "course_title": "The fifth element",
            "course_code": "TFE222",
            "passing_grade": 70,
            "school_id": self.admin.school_id
        }

        response = self.client.post("/api/courses/", data=json.dumps(payload),
                                    headers={
                                        "Authorization": f"Bearer {self.access_token}",
                                        "content-type": "application/json"
                                    })
        
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 201)
        self.assertIn("course", data)
    
    def test_get_courses(self):
        """Testing fetching courses via GET /api/courses"""

        payload = {
            "school_id": f"{self.admin.school_id}"
        }

        response = self.client.get("/api/courses/", data=json.dumps(payload),
                                   headers={
                                       "Authorization": f"Bearer {self.access_token}",
                                       "content-type": "application/json"
                                   })
        

        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertIn("courses", data)
    
    def test_get_course(self):
        """Testing course retrieval via GET /api/courses/<course_code>"""

        response = self.client.get(f"/api/courses/{self.course.course_code}", 
                                   headers={
                                       "Authorization": f"Bearer {self.access_token}",
                                       "content-type": "application/json"
                                   })
        
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertIn("course", data)
    
    def test_course_update(self):
        """Testing course update via PATCH /api/courses/<course_code>"""

        payload = {
            "course_title": "TTO222",
            "passing_grade": 70
        }


        response = self.client.patch(f"/api/courses/{self.course.course_code}", 
                                   data=json.dumps(payload), headers={
                                       "Authorization": f"Bearer {self.access_token}",
                                       "content-type": "application/json"
                                   })
        
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertIn("course", data)
    
#This not supposed to pass 200 as response code review
    def test_course_update_unallowed(self):
        """Testing course update via PATCH /api/courses/<course_code>"""

        payload = {
            "course_title": "Ninja tactics",
            "passing_grade": 70,
            "course_code": "TT0222"
        }


        response = self.client.patch(f"/api/courses/{self.course.course_code}", 
                                   data=json.dumps(payload), headers={
                                       "Authorization": f"Bearer {self.access_token}",
                                       "content-type": "application/json"
                                   })
        
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 422)
    
    def test_delete_course(self):
        """Testing course update via DELETE /api/courses/<course_code>"""

        response = self.client.delete(f"/api/courses/{self.course.course_code}", 
                                    headers={
                                       "Authorization": f"Bearer {self.access_token}",
                                       "content-type": "application/json"
                                   })
        
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 202)
    

