import os

resume_dir = "uploads/resumes/"
os.makedirs(resume_dir, exist_ok=True)

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'Han5h1th@QASDR')  # Used for session security
    DEBUG = True  # Enable/disable debug mode
    TESTING = False  # Set to True for testing environment
    UPLOAD_FOLDER = 'uploads/resumes/'
    SQLALCHEMY_DATABASE_URI = os.getenv(
        'DATABASE_URL',
        'mysql+pymysql://user:pwd@localhost/preppal'
    )  # Update with your MySQL credentials
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # Disable event system overhead