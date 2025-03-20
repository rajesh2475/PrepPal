from flask import render_template, Blueprint, request, jsonify

# Blueprint for interview-related routes
interview_bp = Blueprint('interview', __name__)

@interview_bp.route('/mock_interview')
def mock_interview():
    """
    API endpoint to render the mock interview page.
    """
    try:
        return render_template('mock_interview.html')
    except Exception as e:
        # Log the error and return a generic error message
        return f"An error occurred while loading the mock interview page: {str(e)}", 500

@interview_bp.route("/schedule_interview", methods=["POST"])
def schedule_interview_api():
    """
    API endpoint to schedule an interview for a candidate.
    """
    try:
        data = request.json
        candidate_id = data.get("email")
        interview_date = data.get("interview_date")
        job_id = data.get("job_id")

        if not candidate_id or not interview_date or not job_id:
            return jsonify({"success": False, "message": "Missing required fields"}), 400

        # Placeholder for scheduling logic
        # success = schedule_interview(candidate_id, interview_date, job_id)

        # Simulate success for now
        return jsonify({"success": True, "message": "Interview scheduled successfully!"})
        # Uncomment the following if scheduling logic is implemented
        # if success:
        #     return jsonify({"success": True, "message": "Interview scheduled successfully!"})
        # else:
        #     return jsonify({"success": False, "message": "Failed to schedule interview"}), 500
    except Exception as e:
        # Log the error and return a generic error message
        return jsonify({"success": False, "message": f"An error occurred: {str(e)}"}), 500