# security.py — Password hashing and JWT token utilities.
# Keeping security logic in one file makes it easy to audit,
# rotate algorithms, or swap libraries without touching view code.

import os
from datetime import datetime, timedelta, timezone

from jose import JWTError, jwt
from passlib.context import CryptContext

# CryptContext handles hashing and verification.
# bcrypt is intentionally slow (configurable work factor) — this
# makes brute-force attacks computationally expensive.
# MD5 and SHA-256 are fast by design — great for checksums, terrible
# for passwords because attackers can test billions of guesses per second.
pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

SECRET_KEY = os.environ.get('JWT_SECRET', 'dev-jwt-secret-replace-before-production')
ALGORITHM  = 'HS256'
TOKEN_EXPIRY_MINUTES = 30


def get_password_hash(plain_password: str) -> str:
    """Hash a plain-text password — call this at registration time only"""
    return pwd_context.hash(plain_password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Returns True if the plain password matches the stored hash"""
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict) -> str:
    """
    Creates a signed JWT. The payload (data) is base64-encoded, NOT encrypted.
    Never put sensitive data like passwords or credit card numbers in a JWT —
    anyone who gets the token can decode the payload.
    """
    payload = data.copy()
    payload['exp'] = datetime.now(timezone.utc) + timedelta(minutes=TOKEN_EXPIRY_MINUTES)
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def decode_access_token(token: str) -> dict:
    """Decodes and validates a JWT. Raises JWTError if invalid or expired."""
    return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
