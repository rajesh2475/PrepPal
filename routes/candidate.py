from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename
from extensions import db  # Import db from extensions.py
import os
from models import Candidate, JobOpening
from utils import validate_resume


candidate_bp = Blueprint('candidate', __name__)
ALLOWED_EXTENSIONS = {'pdf', 'docx'}

def allowed_file(filename):
    """
    Check if the uploaded file has an allowed extension.
    """
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@candidate_bp.route('/add_candidate', methods=['POST'])
def add_candidate():
    """
    API endpoint to add a candidate to a job.
    """
    try:
        job_id = request.form.get('job_id')
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        candidate_experience = request.form.get('experience')

        if 'resume' not in request.files:
            return jsonify({"success": False, "message": "No file uploaded"}), 400

        file = request.files['resume']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join('uploads/resumes/', filename)
            file.save(filepath)

            # Check if the job exists
            job = JobOpening.query.get(job_id)
            if not job:
                return jsonify({"success": False, "message": "Job not found"}), 404
            
            # AI/ML Resume Validation
            is_valid, score = validate_resume(filepath, job_id, candidate_experience)

            if not is_valid:
                return jsonify({"success": False, "message": f"Resume not a good fit (Score: {score})"}), 400

            # Save candidate to the database
            new_candidate = Candidate(
                name=name,
                email=email,
                phone=phone,
                resume=filepath,
                score=score,  # Placeholder for AI/ML score
                job_id=job_id
            )
            db.session.add(new_candidate)
            db.session.commit()

            return jsonify({"success": True, "message": "Candidate added successfully!"})
        else:
            return jsonify({"success": False, "message": "Invalid file format"}), 400
    except Exception as e:
        return jsonify({"success": False, "message": f"An error occurred: {str(e)}"}), 500

@candidate_bp.route('/candidates/<int:job_id>', methods=['GET'])
def get_candidates(job_id):
    """
    API endpoint to retrieve all candidates for a specific job.
    """
    try:
        job = JobOpening.query.get(job_id)
        if job:
            candidates = Candidate.query.filter_by(job_id=job_id).all()
            return jsonify([{
                "id": candidate.id,
                "name": candidate.name,
                "email": candidate.email,
                "phone": candidate.phone,
                "resume": candidate.resume,
                "score": candidate.score
            } for candidate in candidates])
        return jsonify({"success": False, "message": "Job not found"}), 404
    except Exception as e:
        return jsonify({"success": False, "message": f"An error occurred: {str(e)}"}), 500

@candidate_bp.route("/remove_candidate/<int:job_id>/<email>", methods=["DELETE"])
def delete_candidate(job_id, email):
    """
    API endpoint to remove a candidate from a job.
    """
    try:
        candidate = Candidate.query.filter_by(job_id=job_id, email=email).first()
        if candidate:
            db.session.delete(candidate)
            db.session.commit()
            return jsonify({"success": True, "message": "Candidate removed successfully!"})
        else:
            return jsonify({"success": False, "message": "Candidate not found"}), 404
    except Exception as e:
        return jsonify({"success": False, "message": f"An error occurred: {str(e)}"}), 500
