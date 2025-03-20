from flask import Blueprint, render_template, session, redirect, url_for, flash, request
from forms import LoginForm, SignupForm

# Blueprint for main routes
main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def home():
    """
    API endpoint to render the home page.
    Displays login and signup forms if the user is not logged in.
    """
    try:
        # if 'user' in session:  # Check if user is logged in
        #     return redirect(url_for('jobs.positions'))

        login_form = LoginForm()
        signup_form = SignupForm()
        return render_template('home.html', login_form=login_form, signup_form=signup_form)
    except Exception as e:
        # Log the error and redirect to a generic error page or flash an error message
        flash(f"An error occurred while loading the home page: {str(e)}", "danger")
        return redirect(url_for('main.home'))