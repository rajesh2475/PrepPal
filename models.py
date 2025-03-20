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
    __tablename__ = 'candidates'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    email = db.Column(db.String(255))
    phone = db.Column(db.String(50))
    resume = db.Column(db.String(255))
    score = db.Column(db.Float)
    job_id = db.Column(db.Integer, db.ForeignKey('job_openings.id'))
