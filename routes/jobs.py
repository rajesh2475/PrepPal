from flask import Blueprint, render_template, session, redirect, url_for, flash, request
from extensions import db  # Import db from extensions.py
from models import JobOpening, Candidate  # Import models for the tables

# Blueprint for job-related routes
jobs_bp = Blueprint('jobs', __name__)

@jobs_bp.route('/job/<int:job_id>')
def job_details(job_id):
    """
    API endpoint to display details of a specific job.
    """
    try:
        job = JobOpening.query.get(job_id)
        if not job:
            flash("Job not found!", "danger")
            return redirect(url_for('jobs.positions'))  # Redirect if job not found
        return render_template("job_details.html", job=job.to_dict())
    except Exception as e:
        raise e

@jobs_bp.route('/positions', methods=['GET'])
def positions():
    """
    API endpoint to display all job positions.
    """
    try:
        job_openings = JobOpening.query.all()  # Fetch all job openings from the database
        return render_template('positions.html', positions=job_openings)
    except Exception as e:
        flash(f"An error occurred while loading positions: {str(e)}", "danger")
        return redirect(url_for('main.home'))

@jobs_bp.route('/job/save', methods=['POST'])
def save_job():
    """
    API endpoint to save or update a job.
    """
    try:
        job_id = request.form.get("job_id")
        job_data = {
            "position": request.form["position"],
            "experience": request.form["experience"],
            "vacancies": int(request.form["vacancies"]),
            "location": request.form["location"],
            "must_have": request.form["must_have"],
            "good_to_have": request.form["good_to_have"],
            "description": request.form["description"],
            "role": request.form["role"],
            "education": request.form["education"],
            "employment_type": request.form["employment_type"]
        }

        if job_id:
            # Update an existing job
            job = JobOpening.query.get(job_id)
            if job:
                for key, value in job_data.items():
                    setattr(job, key, value)
                db.session.commit()
                flash("Job updated successfully!", "success")
            else:
                flash("Job not found!", "danger")
        else:
            # Add a new job
            new_job = JobOpening(**job_data)
            db.session.add(new_job)
            db.session.commit()
            flash("Job added successfully!", "success")

        return redirect(url_for('jobs.positions'))
    except Exception as e:
        flash(f"An error occurred while saving the job: {str(e)}", "danger")
        return redirect(url_for('jobs.positions'))

@jobs_bp.route('/job/delete/<int:job_id>', methods=['POST'])
def delete_job(job_id):
    """
    API endpoint to delete a job.
    """
    try:
        job = JobOpening.query.get(job_id)
        if job:
            db.session.delete(job)
            db.session.commit()
            flash("Job deleted successfully!", "success")
        else:
            flash("Job not found!", "danger")
        return redirect(url_for('jobs.positions'))
    except Exception as e:
        flash(f"An error occurred while deleting the job: {str(e)}", "danger")
        return redirect(url_for('jobs.positions'))