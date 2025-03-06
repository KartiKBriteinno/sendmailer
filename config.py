class Config:
    SECRET_KEY = 'your-secret-key'  # Replace with a secure key
    SQLALCHEMY_DATABASE_URI = 'sqlite:///init_db.py'  # SQLite for simplicity
    SQLALCHEMY_TRACK_MODIFICATIONS = False