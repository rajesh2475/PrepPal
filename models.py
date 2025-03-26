"""
Created by: Rajesh M
Date: June 24, 2024
Description: Database models for the PrepPal application, including JobOpening, Candidate, Interview, and ChatHistory.
"""

from extensions import db  # Import db from extensions.py

class JobOpening(db.Model):
    __tablename__ = 'job_openings'
    id = db.Column(db.Integer, primary_key=True)
    position = db.Column(db.String(255), nullable=False)
    experience = db.Column(db.String(50))
    vacancies = db.Column(db.Integer)
    location = db.Column(db.String(255))
    must_have = db.Column(db.Text)  # Comma-separated string
    good_to_have = db.Column(db.Text)  # Comma-separated string
    description = db.Column(db.Text)
    role = db.Column(db.String(255))
    education = db.Column(db.String(255))
    employment_type = db.Column(db.String(50))
    candidates = db.relationship('Candidate', backref='job', cascade="all, delete-orphan")

    def to_dict(self):
        """
        Convert the JobOpening object into a dictionary.
        """
        return {
            "id": self.id,
            "position": self.position,
            "experience": self.experience,
            "vacancies": self.vacancies,
            "location": self.location,
            "must_have": self.must_have,
            "good_to_have": self.good_to_have,
            "description": self.description,
            "role": self.role,
            "education": self.education,
            "employment_type": self.employment_type
        }

class Candidate(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True)
    phone = db.Column(db.String(15))
    resume_link = db.Column(db.String(255))
    chat_id = db.Column(db.String(50), unique=True)
    score = db.Column(db.Float)
    job_id = db.Column(db.Integer)

class Interview(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    candidate_id = db.Column(db.Integer, db.ForeignKey('candidate.id'), nullable=False)
    interview_link = db.Column(db.String(255), unique=True, nullable=False)
    status = db.Column(db.String(50), default="Scheduled")  # e.g., Scheduled, Completed
    chat_id = db.Column(db.String(100), unique=True, nullable=True)

class ChatHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    chat_id = db.Column(db.String(100), unique=True, nullable=False)
    questions = db.Column(db.Text, nullable=False)  # JSON string of questions
    responses = db.Column(db.Text, nullable=True)  # JSON string of answers
