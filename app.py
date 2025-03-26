from flask import Flask
from config import Config
from extensions import db  # Import db from extensions.py
from routes.main import main_bp
from routes.auth import auth_bp
from routes.candidate import candidate_bp
from routes.interview import interview_bp, socketio
from routes.chat_gpt import chat_bp
from routes.jobs import jobs_bp
from flask_session import Session

def create_app():
    app = Flask(__name__)

    # Load configuration
    app.config.from_object(Config)

    # Initialize database
    db.init_app(app)
    app.config['SESSION_TYPE'] = 'filesystem'  # Store sessions in the filesystem
    app.config['SESSION_PERMANENT'] = False
    Session(app)

    # Register blueprints
    app.register_blueprint(main_bp)
    app.register_blueprint(interview_bp, url_prefix='/interview')
    app.register_blueprint(chat_bp, url_prefix='/chat')
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(candidate_bp, url_prefix='/candidate')
    app.register_blueprint(jobs_bp, url_prefix='/jobs')
    
    socketio.init_app(app, cors_allowed_origins="*") # ✅ Initialize Flask-SocketIO
    return app