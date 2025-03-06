from flask import Flask
from sqlalchemy import create_engine, text
from sqlalchemy.orm import scoped_session, sessionmaker
from flask_login import LoginManager
from config import Config
import os

engine = create_engine(Config.SQLALCHEMY_DATABASE_URI, pool_size=5, max_overflow=10, pool_timeout=30)
db_session = scoped_session(sessionmaker(bind=engine))
login_manager = LoginManager()

def create_app():
    # Explicitly set both template_folder and static_folder
    app = Flask(__name__,
                template_folder=os.path.join(os.path.dirname(__file__), '..', 'templates'),
                static_folder=os.path.join(os.path.dirname(__file__), '..', 'static'))
    app.config.from_object(Config)

    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    from app.models import User
    @login_manager.user_loader
    def load_user(user_id):
        return db_session.get(User, int(user_id))

    from app.auth import auth as auth_bp
    from app.routes import routes as routes_bp
    app.register_blueprint(auth_bp)
    app.register_blueprint(routes_bp)

    @app.teardown_request
    def remove_session(ex=None):
        db_session.remove()

    with app.app_context():
        from app import models
        with engine.connect() as connection:
            connection.execute(text("CREATE TABLE IF NOT EXISTS user (id INTEGER PRIMARY KEY, username TEXT UNIQUE, password TEXT, smtp_host TEXT, smtp_port INTEGER, smtp_username TEXT, smtp_password TEXT, credits INTEGER DEFAULT 0, is_banned BOOLEAN DEFAULT FALSE)"))
            connection.execute(text("CREATE TABLE IF NOT EXISTS campaign (id INTEGER PRIMARY KEY, user_id INTEGER, subject TEXT, content TEXT, status TEXT, sent_count INTEGER DEFAULT 0, FOREIGN KEY(user_id) REFERENCES user(id))"))
            connection.execute(text("CREATE TABLE IF NOT EXISTS notification (id INTEGER PRIMARY KEY, user_id INTEGER, message TEXT, FOREIGN KEY(user_id) REFERENCES user(id))"))
            connection.execute(text("CREATE TABLE IF NOT EXISTS email_status (id INTEGER PRIMARY KEY, campaign_id INTEGER, recipient TEXT, sent BOOLEAN DEFAULT FALSE, opened BOOLEAN DEFAULT FALSE, bounced BOOLEAN DEFAULT FALSE, responded BOOLEAN DEFAULT FALSE, unsubscribed BOOLEAN DEFAULT FALSE, FOREIGN KEY(campaign_id) REFERENCES campaign(id))"))
            connection.commit()

    return app

def teardown_app(exception):
    db_session.remove()