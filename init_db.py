from app import create_app, db_session
from app.models import User, Base
from werkzeug.security import generate_password_hash
from sqlalchemy import create_engine

app = create_app()
engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])

with app.app_context():
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    
    new_admin = User(
        username='admin',
        password=generate_password_hash('admin'),
        smtp_host='smtp.gmail.com',
        smtp_port=587,
        smtp_username='powerlineresearchpublication@gmail.com',  # Replace with your Gmail
        smtp_password='reeq jitq bgrp tocf'      # Replace with Gmail App Password
    )
    db_session.add(new_admin)
    db_session.commit()
    print("Database reset and admin user added with SMTP details.")