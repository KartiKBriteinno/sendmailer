import smtplib
from email.mime.text import MIMEText
from app.models import Campaign, EmailStatus
from app import db_session

def send_bulk_emails(user, recipients, subject, content):
    # Validate SMTP details
    if not all([user.smtp_host, user.smtp_port, user.smtp_username, user.smtp_password]):
        print("Missing SMTP details for user:", user.username)
        return

    # Create a new SMTP connection
    try:
        server = smtplib.SMTP(user.smtp_host, user.smtp_port)
        server.starttls()
        server.login(user.smtp_username, user.smtp_password)
    except Exception as e:
        print(f"Failed to connect to SMTP server: {e}")
        return

    campaign = Campaign(user_id=user.id, subject=subject, content=content, status='in_progress', sent_count=0)
    db_session.add(campaign)
    db_session.commit()

    sent_count = 0
    for recipient in recipients:
        recipient = recipient.strip()
        email_status = EmailStatus(campaign_id=campaign.id, recipient=recipient)
        db_session.add(email_status)
        try:
            tracking_url = f"http://127.0.0.1:5000/track_open/{campaign.id}/{recipient}"
            content_with_pixel = content + f'<img src="{tracking_url}" style="display:none;" alt="" width="1" height="1">'
            msg = MIMEText(content_with_pixel, 'html')
            msg['Subject'] = subject
            msg['From'] = user.smtp_username
            msg['To'] = recipient
            server.send_message(msg)
            email_status.sent = True
            sent_count += 1
        except Exception as e:
            print(f"Failed to send to {recipient}: {e}")
            email_status.bounced = True
        db_session.commit()

    campaign.sent_count = sent_count
    campaign.status = 'sent' if sent_count > 0 else 'failed'
    db_session.commit()

    server.quit()