from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from database import get_user, add_user, store_reset_token, users
import secrets
import hashlib

auth_bp = Blueprint('auth', __name__)

from flask_oauthlib.client import OAuth

oauth = OAuth()

google = oauth.remote_app(
    'google',
    consumer_key='GOOGLE_CLIENT_ID',  # Replace with your Google Client ID
    consumer_secret='GOOGLE_CLIENT_SECRET', # Replace with your Google Client Secret
    request_token_params={'scope': 'email'},
    base_url='https://www.googleapis.com/oauth2/v1/',
    request_token_url=None,
    access_token_method='POST',
    access_token_url='https://accounts.google.com/o/oauth2/token',
    authorize_url='https://accounts.google.com/o/oauth2/auth',
)

github = oauth.remote_app(
    'github',
    consumer_key='GITHUB_CLIENT_ID',   # Replace with your Github Client ID
    consumer_secret='GITHUB_CLIENT_SECRET',  # Replace with your Github Client Secret
    request_token_params={'scope': 'user:email'},
    base_url='https://api.github.com/',
    request_token_url=None,
    access_token_method='POST',
    access_token_url='https://github.com/login/oauth/access_token',
    authorize_url='https://github.com/login/oauth/authorize'
)

@auth_bp.route('/login/google')
def google_login():
    return google.authorize(url_for('auth.google_authorized', _external=True))

@auth_bp.route('/login/github')
def github_login():
    return github.authorize(url_for('auth.github_authorized', _external=True))

@auth_bp.route('/login/google/authorized')
def google_authorized():
    resp = google.authorized_response()
    if resp is None:
        flash('Access denied: reason=' + request.args['error_reason'] + ' error=' + request.args['error_description'])
        return redirect(url_for('auth.login'))
    session['google_token'] = (resp['access_token'], '')
    user_info = google.get('userinfo').data
    email = user_info['email']
    username = email.split('@')[0]  # Use email as username
    user = get_user(username)
    if not user:
        add_user(username, 'google_user')  # Add user without password
    session['username'] = username
    return redirect(url_for('chat'))

@auth_bp.route('/login/github/authorized')
def github_authorized():
    resp = github.authorized_response()
    if resp is None:
        flash('Access denied: reason=' + request.args['error_reason'] + ' error=' + request.args['error_description'])
        return redirect(url_for('auth.login'))
    session['github_token'] = (resp['access_token'], '')
    user_info = github.get('user').data
    username = user_info['login']
    user = get_user(username)
    if not user:
        add_user(username, 'github_user')  # Add user without password
    session['username'] = username
    return redirect(url_for('chat'))

# In real app, use password hashing and salting
def validate_password(user, password):
    if user and user['password'] == password:
        return True
    return False


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = get_user(username)

        if user and validate_password(user, password):  # In real app, use password hashing
            session['username'] = username
            return redirect(url_for('chat'))
        else:
            flash('Invalid username or password')
    return render_template('login.html')

@auth_bp.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        if get_user(username):
            flash('Username already exists')
        else:
            add_user(username, password)
            session['username'] = username
            return redirect(url_for('chat'))
    return render_template('signup.html')

@auth_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

@auth_bp.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        email = request.form['email']
        user = next((u for u in users.values() if u['username'] == email), None) # Assuming email is username
        if not user:
            flash('Email not found.')
            return render_template('forgot_password.html')

        token = secrets.token_hex(16)
        hashed_token = hashlib.sha256(token.encode()).hexdigest()
        store_reset_token(email, hashed_token)
        reset_link = url_for('auth.reset_password', token=token, _external=True)
        print(f"Reset link: {reset_link}")  # In real app, send email
        flash('Reset link has been sent to your email.')
        return render_template('forgot_password.html')
    return render_template('forgot_password.html')

@auth_bp.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if request.method == 'POST':
        print(f"Token: {token}")
        email = get_email_from_token(token)
        print(f"Email: {email}")
        if not email:
            flash('Invalid reset token.')
            return redirect(url_for('auth.login'))

        password = request.form['password']
        confirm_password = request.form['confirm_password']

        if password != confirm_password:
            flash('Passwords do not match.')
            return render_template('reset_password.html', token=token)

        user = next((u for u in users.values() if u['username'] == email), None) # Assuming email is username
        if not user:
            flash('User not found.')
            return redirect(url_for('auth.login'))
        update_password(email, password) # Assuming email is username
        flash('Password reset successfully. Please login.')
        return redirect(url_for('auth.login'))
    return render_template('reset_password.html')
