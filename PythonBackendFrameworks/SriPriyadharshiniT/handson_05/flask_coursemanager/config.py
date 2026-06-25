# config.py — All environment-specific settings live here.
# Keeping config separate from app logic means you can swap
# settings for dev/staging/production without touching any view code.

import os

class Config:
    # Use an environment variable in production — never hardcode secrets
    SECRET_KEY             = os.environ.get('SECRET_KEY', 'dev-secret-change-in-prod')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'sqlite:///courses.db')
    # Disabling modification tracking saves memory — we don't need it
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = True
