import unittest
from app import app, db
from models import User

class TestApp(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'  # Use a test database
        db.init_app(app)
        self.client = app.test_client()

        # Create the test database tables
        with app.app_context():
            db.create_all()

    def tearDown(self):
        # Drop the test database tables
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_home_page(self):
        # Test if the home page returns a 200 status code when authenticated
        user = User(public_id="test_user_id", name="Test User", email="test@example.com", password="test_password")
        db.session.add(user)
        db.session.commit()
        access_token = "your_access_token_here"  # Replace with a valid access token
        headers = {"Authorization": f"Bearer {access_token}"}
        response = self.client.get('/', headers=headers)
        self.assertEqual(response.status_code, 200)

    def test_register_route(self):
        # Test if the register route returns a 200 status code
        response = self.client.get('/register')
        self.assertEqual(response.status_code, 200)

    def test_login_route(self):
        # Test if the login route returns a 200 status code
        response = self.client.get('/login')
        self.assertEqual(response.status_code, 200)

    def test_logout_route(self):
        # Test if the logout route returns a 302 (redirect) status code when authenticated
        user = User(public_id="test_user_id", name="Test User", email="test@example.com", password="test_password")
        db.session.add(user)
        db.session.commit()
        access_token = "your_access_token_here"  # Replace with a valid access token
        headers = {"Authorization": f"Bearer {access_token}"}
        response = self.client.get('/logout', headers=headers)
        self.assertEqual(response.status_code, 302)

    def test_google_route(self):
        # Test if the Google OAuth route returns a 302 (redirect) status code
        response = self.client.get('/google')
        self.assertEqual(response.status_code, 302)

    # Add more test methods for other routes as needed

if __name__ == '__main__':
    unittest.main()