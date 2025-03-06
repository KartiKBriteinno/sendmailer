from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user
from app import db_session
from app.models import User
from werkzeug.security import generate_password_hash, check_password_hash

auth = Blueprint('auth', __name__)

@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        
        if password != confirm_password:
            flash('Passwords do not match.')
            return render_template('register.html')
        
        existing_user = db_session.query(User).filter_by(username=username).first()
        if existing_user:
            flash('Username already taken.')
            return render_template('register.html')
        
        new_user = User(username=username, password=generate_password_hash(password))
        db_session.add(new_user)
        db_session.commit()
        flash('Registration successful! Please log in.')
        return redirect(url_for('auth.login'))
    
    return render_template('register.html')

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        smtp_host = request.form['smtp_host']
        smtp_port = request.form['smtp_port']
        smtp_username = request.form['smtp_username']
        smtp_password = request.form['smtp_password']

        user = db_session.query(User).filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            user.smtp_host = smtp_host
            user.smtp_port = int(smtp_port)
            user.smtp_username = smtp_username
            user.smtp_password = smtp_password
            db_session.commit()
            login_user(user)
            return redirect(url_for('routes.dashboard'))
        else:
            flash('Invalid credentials or user not found.')
    return render_template('login.html')

@auth.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('auth.login'))