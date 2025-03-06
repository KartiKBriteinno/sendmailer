from flask_login import UserMixin
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Text
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(UserMixin, Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    password = Column(String(100), nullable=False)
    smtp_host = Column(String(100))
    smtp_port = Column(Integer)
    smtp_username = Column(String(100))
    smtp_password = Column(String(100))
    credits = Column(Integer, default=0)
    is_banned = Column(Boolean, default=False)

class Campaign(Base):
    __tablename__ = 'campaign'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    subject = Column(String(200))
    content = Column(Text)
    status = Column(String(50))  # Overall status (e.g., 'sent', 'in_progress')
    sent_count = Column(Integer, default=0)

class EmailStatus(Base):
    __tablename__ = 'email_status'
    id = Column(Integer, primary_key=True)
    campaign_id = Column(Integer, ForeignKey('campaign.id'))
    recipient = Column(String(100))  # Email address
    sent = Column(Boolean, default=False)
    opened = Column(Boolean, default=False)
    bounced = Column(Boolean, default=False)
    responded = Column(Boolean, default=False)
    unsubscribed = Column(Boolean, default=False)

class Notification(Base):
    __tablename__ = 'notification'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    message = Column(Text)