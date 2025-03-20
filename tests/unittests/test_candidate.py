import unittest
from app import create_app

class TestCandidateRoutes(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = create_app()
        cls.app.config['TESTING'] = True
        cls.client = cls.app.test_client()

    def test_add_candidate(self):
        data = {
            'job_id': 1,
            'name': 'John Doe',
            'email': 'john.doe@example.com',
            'phone': '1234567890',
            'resume': 'path/to/resume.pdf',
            "experience": "2 years",
        }
        response = self.client.post('/candidate/add_candidate', data=data)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Candidate added successfully', response.data)

if __name__ == '__main__':
    unittest.main()