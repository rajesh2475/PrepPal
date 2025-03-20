import unittest
from app import create_app

class TestAuthRoutes(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = create_app()
        cls.app.config['TESTING'] = True
        cls.client = cls.app.test_client()

    def test_login_route(self):
        data = {'email': 'test@example.com', 'password': 'password123'}
        response = self.client.post('/auth/login', data=data)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Login successful', response.data)  # Adjust based on your API response

if __name__ == '__main__':
    unittest.main()