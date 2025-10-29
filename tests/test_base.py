import unittest
from main import create_app
from src.api.utils.database import db
from src.api.config.config import TestingConfig
import tempfile

class BaseTestCase(unittest.TestCase):
    """A base test case."""

    def setUp(self):
        app = create_app(TestingConfig)
        self.test_db_file = tempfile.mkstemp()[1]
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + self.test_db_file
        app.config['TESTING'] = True

        with app.app_context():
            db.create_all()
        app.app_context().push()

        self.client = app.test_client()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
