import unittest
import os
from app import create_app
from models import db, User, Student
from config import Config

class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'  # Use in-memory DB for tests
    WTF_CSRF_ENABLED = False  # Disable CSRF for testing forms easier

class StudentSystemTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestConfig)
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_auth_pages_accessible(self):
        # Login page should return 200 OK
        response = self.client.get('/login')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Welcome Back', response.data)

        # Register page should return 200 OK
        response = self.client.get('/register')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Create Account', response.data)

    def test_social_login(self):
        # Test Google login redirection and user creation
        response = self.client.get('/social-login/google', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Successfully logged in with Google.', response.data)
        
        user = User.query.filter_by(email='google_user@example.com').first()
        self.assertIsNotNone(user)
        
        # Test GitHub login redirection and user creation
        response = self.client.get('/social-login/github', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Successfully logged in with Github.', response.data)
        
        user = User.query.filter_by(email='github_user@example.com').first()
        self.assertIsNotNone(user)

    def test_dashboard_redirects_unauthenticated(self):
        # Dashboard should redirect (302) to login if not logged in
        response = self.client.get('/dashboard')
        self.assertEqual(response.status_code, 302)
        self.assertIn('/login', response.headers['Location'])

    def test_user_registration_and_login(self):
        # Test registering a user
        response = self.client.post('/register', data={
            'email': 'admin@test.com',
            'password': 'password123',
            'confirm_password': 'password123'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Registration successful!', response.data)

        # Verify password is secure (hashed)
        user = User.query.filter_by(email='admin@test.com').first()
        self.assertIsNotNone(user)
        self.assertNotEqual(user.password_hash, 'password123')
        self.assertTrue(user.check_password('password123'))
        self.assertFalse(user.check_password('wrongpassword'))

        # Test logging in
        response = self.client.post('/login', data={
            'email': 'admin@test.com',
            'password': 'password123'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Logged in successfully.', response.data)
        self.assertIn(b'admin@test.com', response.data)

    def test_student_crud(self):
        # First, register and log in
        self.client.post('/register', data={
            'email': 'admin@test.com',
            'password': 'password123',
            'confirm_password': 'password123'
        })
        self.client.post('/login', data={
            'email': 'admin@test.com',
            'password': 'password123'
        })

        # Create a student record
        response = self.client.post('/students/add', data={
            'name': 'Alice Smith',
            'email': 'alice@test.com',
            'phone': '1234567890',
            'department': 'Computer Science',
            'semester': '3rd Semester',
            'address': '123 Main St'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Student &#39;Alice Smith&#39; added successfully.", response.data)

        # Check database records
        student = Student.query.filter_by(email='alice@test.com').first()
        self.assertIsNotNone(student)
        self.assertEqual(student.name, 'Alice Smith')
        self.assertEqual(student.department, 'Computer Science')

        # Test duplicate email validation
        response = self.client.post('/students/add', data={
            'name': 'Bob Smith',
            'email': 'alice@test.com',  # Duplicate email!
            'phone': '0987654321',
            'department': 'Information Technology',
            'semester': '1st Semester',
            'address': '456 Oak Ave'
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'A student with this email address is already registered.', response.data)

        # Search for the student
        response = self.client.get('/students?search=Alice')
        self.assertIn(b'Alice Smith', response.data)

        # Edit student details
        response = self.client.post(f'/students/edit/{student.id}', data={
            'name': 'Alice Johnson',
            'email': 'alice.j@test.com',
            'phone': '1234567890',
            'department': 'Computer Science',
            'semester': '4th Semester',
            'address': '789 Pine Rd'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Student &#39;Alice Johnson&#39; updated successfully.", response.data)

        # Verify database update
        db.session.refresh(student)
        self.assertEqual(student.name, 'Alice Johnson')
        self.assertEqual(student.semester, '4th Semester')

        student_id = student.id
        # Delete student record
        response = self.client.post(f'/students/delete/{student_id}', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Student &#39;Alice Johnson&#39; deleted successfully.", response.data)
        
        # Verify student is gone
        student_check = db.session.get(Student, student_id)
        self.assertIsNone(student_check)

if __name__ == '__main__':
    unittest.main()
