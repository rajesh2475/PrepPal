import unittest
from app import create_app

class TestJobsRoutes(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = create_app()
        cls.app.config['TESTING'] = True
        cls.client = cls.app.test_client()

    def test_positions_route(self):
        response = self.client.get('/jobs/positions')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Job Positions', response.data)  # Adjust based on your template content

if __name__ == '__main__':
    unittest.main()