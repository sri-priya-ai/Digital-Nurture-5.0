from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta

# bcrypt uses a slow hashing algorithm by design (work factor / cost factor).
# MD5 and SHA-256 are fast — an attacker can brute-force millions of guesses/sec.
# bcrypt limits that to thousands, making offline attacks impractical.

ALGO = 'HS256'
JWT_SECRET = 'super-secret-change-in-prod'
TOKEN_EXPIRY_MINS = 30

pwd_ctx = CryptContext(schemes=['bcrypt'], deprecated='auto')


def hash_pwd(raw: str) -> str:
    return pwd_ctx.hash(raw)


def check_pwd(raw: str, hashed: str) -> bool:
    return pwd_ctx.verify(raw, hashed)


def build_token(data: dict) -> str:
    payload = data.copy()
    payload['exp'] = datetime.utcnow() + timedelta(minutes=TOKEN_EXPIRY_MINS)
    return jwt.encode(payload, JWT_SECRET, algorithm=ALGO)


def decode_token(token: str) -> dict:
    return jwt.decode(token, JWT_SECRET, algorithms=[ALGO])
