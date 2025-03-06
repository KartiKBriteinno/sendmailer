from app import create_app, db_session
from app.models import User

app = create_app()

with app.app_context():
    users = db_session.query(User).all()
    print([u.username for u in users])