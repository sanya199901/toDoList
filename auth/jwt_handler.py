# JWT token creation and verification
# Now reads SECRET_KEY from .env via config.py
from jose import jwt, JWTError
from datetime import datetime, timedelta
from config import settings


# Create a JWT token with user's email inside
def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


# Verify a JWT token and return the email inside
# Returns None if token is invalid or expired
def verify_access_token(token: str):
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        email: str = payload.get("sub")
        if email is None:
            return None
        return email
    except JWTError:
        return None
