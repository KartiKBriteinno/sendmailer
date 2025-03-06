from app import create_app, db_session
from app.models import User

app = create_app()

with app.app_context():
    users = db_session.query(User).all()
    for user in users:
        print(f"Username: {user.username}, Password: {user.password}")