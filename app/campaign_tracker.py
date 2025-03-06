from app.models import EmailStatus
from app import db_session

def update_campaign_status(campaign_id, status_data):
    # Placeholder for future real updates (e.g., via tracking pixel)
    pass

def track_campaign(campaign_id):
    emails = db_session.query(EmailStatus).filter_by(campaign_id=campaign_id).all()
    status_summary = {
        'sent': sum(1 for e in emails if e.sent),
        'opened': sum(1 for e in emails if e.opened),
        'bounced': sum(1 for e in emails if e.bounced),
        'responded': sum(1 for e in emails if e.responded),
        'unsubscribed': sum(1 for e in emails if e.unsubscribed),
        'emails': [{'recipient': e.recipient, 'sent': e.sent, 'opened': e.opened, 'bounced': e.bounced, 'responded': e.responded, 'unsubscribed': e.unsubscribed} for e in emails]
    }
    return status_summary