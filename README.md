# Email Sender App

A Flask-based web application for sending bulk HTML emails with user authentication, admin panel, credit system, and campaign tracking.

## Features
- User login with SMTP credentials
- Bulk email sending (500-1000 emails)
- Admin panel to manage users, credits, and bans
- Credit system for email sending limits
- Campaign tracking (sent status; extendable for opened, bounced, etc.)
- Responsive design with sidebar navigation
- Live sending status (simulated)

## Setup
1. Install dependencies: `pip install -r requirements.txt`
2. Run the app: `python run.py`
3. Create an admin user manually in the database:
   - Username: `admin`, Password: `admin`
4. Access at `http://localhost:5000/login`

## Notes
- Use a task queue (e.g., Celery) for large bulk sends.
- Enhance security with password hashing and role-based access.
- Extend campaign tracking with tracking pixels or SMTP responses.