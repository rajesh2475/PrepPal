from flask import render_template, Blueprint

# Blueprint for ChatGPT-related routes
chat_bp = Blueprint('chat', __name__)

@chat_bp.route('/qna')
def qna():
    """
    API endpoint to render the QnA page.
    """
    try:
        return render_template('qna.html')
    except Exception as e:
        # Log the error and return a generic error message
        return f"An error occurred while loading the QnA page: {str(e)}", 500