import os


class AppConfig:
    DB_URI = os.environ.get('DATABASE_URL', 'sqlite:///courses.db')
    APP_SECRET = os.environ.get('SECRET_KEY', 'dev-secret-key-change-me')
    DEBUG_MODE = True
    SQLALCHEMY_DATABASE_URI = DB_URI
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = APP_SECRET
