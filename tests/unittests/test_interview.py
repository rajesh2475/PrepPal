import unittest
import sys
import os

# Add the project root directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

from app import create_app

class TestInterviewRoutes(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = create_app()
        cls.app.config['TESTING'] = True
        cls.client = cls.app.test_client()

    def test_schedule_interview(self):
        data = {
            'candidate_id': 1,
            'interview_date': '2025-03-25',
            'job_id': 1
        }
        response = self.client.post('/interview/schedule_interview', json=data)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Interview scheduled successfully', response.data)

if __name__ == '__main__':
    unittest.main()