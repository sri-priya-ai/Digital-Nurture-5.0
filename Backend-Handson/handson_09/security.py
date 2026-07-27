"""
security.py
Password hashing (bcrypt) and JWT token creation/verification utilities.

Step 89: bcrypt is preferred over MD5/SHA-256 for passwords because bcrypt
is a deliberately SLOW, salted hashing algorithm with a tunable work
factor. MD5 and SHA-256 are designed to be FAST, which is exactly the
wrong property for password storage - fast hashes let an attacker who
steals the password table try billions of guesses per second. bcrypt's
built-in salt also defeats precomputed rainbow-table attacks, and its
work factor can be increased over time as hardware gets faster.
"""

from datetime import datetime, timedelta, timezone
from typing import Optional

from jose import JWTError, jwt
from passlib.context import CryptContext

# ---------------------------------------------------------------------------
# Password hashing
# ---------------------------------------------------------------------------
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


# ---------------------------------------------------------------------------
# JWT
# ---------------------------------------------------------------------------
# NOTE: in a real project this secret MUST come from an environment
# variable / secrets manager, never hard-coded in source control.
SECRET_KEY = "CHANGE_ME_dev_only_secret_key_do_not_use_in_production"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (
        expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def decode_access_token(token: str) -> Optional[dict]:
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError:
        return None
