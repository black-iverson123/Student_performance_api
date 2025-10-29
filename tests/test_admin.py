import json
from test_base import BaseTestCase  
from src.api.models.admin import Admin

def create_admin():
    admin1 = Admin(username="Admin2", email="Admin2@example.com", password="12345",
                   school_name="Jujutsu Kaisen", school_acronym="JJK" ).create()
    admin2 = Admin(username="Admin3", email="Admin3@example.com", password="12345",
                   school_name="Teiko High", school_acronym="TKH" ).create()


class TestAdminRoutes(BaseTestCase):
    def setUp(self):
        super().setUp()
        create_admin()

    def test_create_admin(self):
        """Test admin creation via POST /api/admin/"""

        payload = {
            "username": "admin1",
            "email": "admin1@example.com",
            "password": "admin123",
            "school_name": "Tech High",
            "school_acronym": "TCH"
        }

        response = self.client.post(
            "/api/admin/",
            data=json.dumps(payload),
            content_type="application/json"
        )

        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        self.assertIn("admin", data)
        self.assertEqual(data["admin"]["email"], payload["email"])


    def test_create_registered_admin(self):
        """Test admin creation with missing email via POST /api/admin/"""

        payload = {
            "username": "admin1",
            "email": "Admin2@example.com",
            "password": "admin123",
            "school_name": "Tech High",
            "school_acronym": "TCH"
        }

        response = self.client.post(
            "/api/admin/",
            data=json.dumps(payload),
            content_type="application/json"
        )

        self.assertEqual(response.status_code, 422)
        data = json.loads(response.data)
        self.assertIn("message", data)

    def test_admin_login(self):
        """Test admin login via POST /api/admin/login"""

        payload = {
            "email": "Admin2@example.com",
            "password": "12345"
        }

        response = self.client.post(
            "/api/admin/login",
            data=json.dumps(payload),
            content_type="application/json"
        )

        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn("access_token", data)
        self.assertIn("refresh_token", data)
    
    def test_admin_invalid_login(self):
        """Test admin invalid login via POST /api/admin/login"""

        payload = {
            "email": "Admin24@example.com",
            "password": "12345"
        }

        response = self.client.post(
            "/api/admin/login",
            data=json.dumps(payload),
            content_type="application/json"
        )

        self.assertEqual(response.status_code, 403)
       
    def test_refresh_token_route(self):
        """Test token refresh via endpoint api/admin/refresh"""

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

        token = json.loads(login_response.data)

        refresh_token = token['refresh_token']

        response = self.client.post("" \
        "api/admin/refresh",
        headers={"Authorization": f"Bearer {refresh_token}"})

        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn("access_token", data)
    
    

