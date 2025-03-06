from flask import Blueprint, render_template, request, redirect, url_for, jsonify, Response  # Add Response
from flask_login import login_required, current_user
from app import db_session
from app.models import User, Campaign, Notification, EmailStatus  # Add EmailStatus
from app.email_service import send_bulk_emails
from app.utils import manage_credits
from app.campaign_tracker import track_campaign

routes = Blueprint('routes', __name__)

@routes.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('routes.dashboard'))
    return redirect(url_for('auth.register'))

@routes.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    if current_user.is_banned:
        return "Your account is banned."
    if request.method == 'POST':
        recipients = request.form['recipients'].split(',')
        subject = request.form['subject']
        content = request.form['content']
        if current_user.credits >= len(recipients):
            send_bulk_emails(current_user, recipients, subject, content)
            current_user.credits -= len(recipients)
            db_session.commit()
        else:
            return "Insufficient credits."
    campaigns = db_session.query(Campaign).filter_by(user_id=current_user.id).all()
    notifications = db_session.query(Notification).filter_by(user_id=current_user.id).all()
    return render_template('dashboard.html', campaigns=campaigns, notifications=notifications)

@routes.route('/admin', methods=['GET', 'POST'])
@login_required
def admin_panel():
    if current_user.username != 'admin':
        return "Unauthorized."
    if request.method == 'POST':
        action = request.form['action']
        user_id = request.form['user_id']
        user = db_session.get(User, user_id)
        if action == 'add_credits' or action == 'remove_credits':
            credits = request.form['credits']
            if not credits:
                flash('Please enter a number of credits.')
            else:
                try:
                    credits = int(credits)
                    if credits < 0:
                        flash('Credits cannot be negative.')
                    else:
                        manage_credits(user, action.split('_')[0], credits)
                except ValueError:
                    flash('Invalid credits value. Please enter a number.')
        elif action == 'ban':
            user.is_banned = True
            db_session.commit()
        elif action == 'unban':
            user.is_banned = False
            db_session.commit()
    users = db_session.query(User).all()
    return render_template('admin_panel.html', users=users)

@routes.route('/campaign/<int:campaign_id>')
@login_required
def campaign_status(campaign_id):
    campaign = db_session.get(Campaign, campaign_id) or abort(404)
    return render_template('campaign_status.html', campaign=campaign)

@routes.route('/campaign_status/<int:campaign_id>', methods=['GET'])
@login_required
def get_campaign_status(campaign_id):
    status = track_campaign(campaign_id)
    return jsonify(status)

@routes.route('/track_open/<int:campaign_id>/<path:recipient>')
def track_open(campaign_id, recipient):
    email_status = db_session.query(EmailStatus).filter_by(campaign_id=campaign_id, recipient=recipient).first()
    if email_status and not email_status.opened:
        email_status.opened = True
        db_session.commit()
    # Return a 1x1 transparent pixel
    pixel = b'GIF89a\x01\x00\x01\x00\x80\x00\x00\x00\x00\x00\x00\x00\x00!\xf9\x04\x01\x00\x00\x00\x00,\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02D\x01\x00;'
    return Response(pixel, mimetype='image/gif')

@routes.route('/notifications')
@login_required
def notifications():
    notifications = db_session.query(Notification).filter_by(user_id=current_user.id).all()
    return render_template('notifications.html', notifications=notifications)