from forms import LoginForm, SignupForm
from flask import session, redirect, url_for, flash, Blueprint

# Dummy user database
users = {}

# Blueprint for authentication routes
auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['POST'])
def login():
    """
    API endpoint for user login.
    Validates user credentials and logs them in if successful.
    """
    form = LoginForm()
    try:
        if form.validate_on_submit():
            email = form.email.data
            password = form.password.data

            if email in users and users[email] == password:
                session['user'] = email
                flash('Login successful!', 'success')
                return redirect(url_for('jobs.positions'))
            else:
                flash('Invalid email or password', 'danger')
    except Exception as e:
        flash(f"An error occurred during login: {str(e)}", 'danger')

    return redirect(url_for('main.home'))

@auth_bp.route('/signup', methods=['POST'])
def signup():
    """
    API endpoint for user signup.
    Registers a new user if the email is not already taken.
    """
    form = SignupForm()
    try:
        if form.validate_on_submit():
            email = form.email.data
            password = form.password.data

            if email in users:
                flash('Email already registered', 'warning')
            else:
                users[email] = password
                session['user'] = email
                flash('Signup successful!', 'success')
                return redirect(url_for('jobs.positions'))
    except Exception as e:
        flash(f"An error occurred during signup: {str(e)}", 'danger')

    return redirect(url_for('main.home'))

@auth_bp.route('/logout')
def logout():
    """
    API endpoint for user logout.
    Logs out the current user by clearing the session.
    """
    try:
        session.pop('user', None)
        session.clear()
        flash('You have been logged out.', 'info')
    except Exception as e:
        flash(f"An error occurred during logout: {str(e)}", 'danger')

    return redirect(url_for('main.home'))