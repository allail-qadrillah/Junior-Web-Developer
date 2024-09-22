from flask import Blueprint, redirect, url_for, session

# Create a Blueprint for the authentication routes
auth = Blueprint('auth', __name__)

# * Route endpoint login
@auth.route('/login/<role>')
def login(role):
    # Set the user role in the session
    session['role'] = role

    # Redirect to the products page
    return redirect(url_for('main.products'))