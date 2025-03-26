"""
Created by: Rajesh M
Date: July 22, 2024
Description: Routes for managing interviews, including scheduling, evaluating, and handling AI-driven interviews.
"""

from flask import Flask, request, jsonify, Blueprint
from flask_sqlalchemy import SQLAlchemy
import requests
import pdfplumber
import openai
import uuid
from extensions import db
from models import Candidate, Interview, JobOpening
from send_email import send_email
from config import Config
import time
import os
from flask_socketio import SocketIO
from moviepy.video.io.VideoFileClip import VideoFileClip

socketio = SocketIO()  # ✅ Initialize Flask-SocketIO


interview_bp = Blueprint('interview', __name__)
# https://platform.openai.com/api-keys
openai.api_key = os.getenv("OPENAI_API_KEY")

# Fetch resume text
def fetch_resume_text(resume_link):
    response = requests.get(resume_link)
    if response.status_code == 200:
        with open("temp_resume.pdf", "wb") as f:
            f.write(response.content)
        with pdfplumber.open("temp_resume.pdf") as pdf:
            text = "\n".join(page.extract_text() for page in pdf.pages if page.extract_text())
        return text
    return None

# Generate AI interview questions
def generate_interview_questions(job_description, resume_text):
    prompt = f"""
    Given the job description:
    {job_description}
    
    And the candidate's resume:
    {resume_text}
    
    Generate:
    1. 3 interview questions.
    2. 2 logical programming challenges.
    """
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "system", "content": "Generate structured interview questions."},
                  {"role": "user", "content": prompt}]
    )
    return response["choices"][0]["message"]["content"]

@interview_bp.route('/schedule_interview', methods=['POST'])
def schedule_interview():
    data = request.json
    candidate_email = data.get("candidate_email")
    candidate = Candidate.query.filter_by(email=candidate_email).first()

    if not candidate:
        return jsonify({"error": "Candidate not found"}), 404

    resume_text = fetch_resume_text(candidate.resume_link)
    
    if not resume_text:
        return jsonify({"error": "Failed to process resume"}), 400
    
    JobInfo = JobOpening.query.filter_by(job_id=candidate.job_id).first()
    job_description = JobInfo.description
    questions = generate_interview_questions(job_description, resume_text)
    chat_id = str(uuid.uuid4())

    candidate = Candidate.query.filter_by(email=candidate_email).first()
    candidate.chat_id = chat_id
    db.session.commit()

    interview = Interview(candidate_id=candidate.id, chat_id=chat_id, questions=questions, responses={})
    db.session.add(interview)
    db.session.commit()
    interview_link = f"https://{Config.HOST}:{Config.PORT}/join_interview/{chat_id}"
    send_email(candidate_email, "Your AI Interview", f"Click to join: {interview_link}")

    return jsonify({"success": True, "chat_id": chat_id, "interview_link": interview_link, "questions": questions})


def evaluate_answers(questions, responses):
    prompt = f"""
    Given these questions:
    {questions}
    
    And these responses:
    {responses}
    
    Provide a score (0-100%) and feedback.
    """
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "system", "content": "Evaluate candidate responses."},
                  {"role": "user", "content": prompt}]
    )
    return response["choices"][0]["message"]["content"]

@interview_bp.route('/evaluate/<chat_id>', methods=['GET'])
def evaluate_interview(chat_id):
    interview = Interview.query.filter_by(chat_id=chat_id).first()
    if not interview:
        return jsonify({"error": "Interview not found"}), 404

    evaluation = evaluate_answers(interview.questions, interview.responses)
    interview.evaluation = evaluation
    db.session.commit()
    return jsonify({"evaluation": evaluation})


@socketio.on("join_interview")
def handle_join_interview(data):
    chat_id = data.get("chat_id")
    interview = Interview.query.filter_by(chat_id=chat_id).first()
    if not interview:
        return

    # Fetch stored questions
    questions = interview.questions

    for question in questions:
        socketio.emit("interview_question", {"question": question}, room=chat_id)
        time.sleep(5)  # Wait for response


def process_video_response(video_file):
    """Convert video to audio & transcribe response"""
    audio_text = speech_to_text_whisper(video_file)
    
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "Evaluate this response: " + audio_text}
        ]
    )
    return response["choices"][0]["message"]["content"]


def speech_to_text_whisper(video_file):
    # Extract audio from video
    video = VideoFileClip(video_file)
    audio_path = "temp_audio.mp3"
    video.audio.write_audiofile(audio_path)

    # Transcribe audio using OpenAI Whisper
    with open(audio_path, "rb") as file:
        response = openai.Audio.transcribe("whisper-1", file)

    os.remove(audio_path)  # Cleanup
    return response.get("text", "")