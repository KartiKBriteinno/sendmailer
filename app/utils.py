from app.models import Notification
from app import db_session

def add_notification(user_id, message):
    """Add a notification for a user."""
    notification = Notification(user_id=user_id, message=message)
    db_session.add(notification)
    db_session.commit()

def manage_credits(user, action, amount):
    """Manage user credits and notify them."""
    if action == 'add':
        user.credits += amount
        add_notification(user.id, f"{amount} credits added to your account.")
    elif action == 'remove':
        user.credits = max(0, user.credits - amount)
        add_notification(user.id, f"{amount} credits removed from your account.")
    db_session.commit()