# jwt from python-jose handles creating and verifying JWT tokens
from jose import jwt, JWTError

# datetime helps us set token expiry time
from datetime import datetime, timedelta

# --- Secret Key ---
# This is used to SIGN the JWT token
# ⚠️ In production, store this in a .env file — never hardcode it
SECRET_KEY = "your_super_secret_key_change_this"

# --- Algorithm ---
# HS256 is the standard algorithm for signing JWT tokens
ALGORITHM = "HS256"

# --- Token Expiry ---
# Token will expire after 30 minutes
# After that, the user needs to log in again
ACCESS_TOKEN_EXPIRE_MINUTES = 30


# --- Create Token ---
# Called after successful login to generate a JWT token
# data = dictionary containing user info (we store email)
def create_access_token(data: dict):

    # Make a copy so we don't modify the original data
    to_encode = data.copy()

    # Set the expiry time — current time + 30 minutes
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    # Add expiry to the token payload
    to_encode.update({"exp": expire})

    # Create and return the signed JWT token string
    token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return token


# --- Verify Token ---
# Called on every protected endpoint to check if token is valid
# Returns the email stored inside the token, or None if invalid
def verify_access_token(token: str):
    try:
        # Decode the token using our secret key
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        # Extract the email we stored when creating the token
        email: str = payload.get("sub")

        # If no email found in token, it's invalid
        if email is None:
            return None

        return email

    except JWTError:
        # Token is expired, tampered, or invalid
        return None
