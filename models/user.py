# BaseModel from Pydantic — used for request body validation
from pydantic import BaseModel, EmailStr


# --- UserRegister ---
# Used when a new user signs up (POST /auth/register)
# This is what the user sends to the API
class UserRegister(BaseModel):
    name: str           # Full name — required
    email: EmailStr     # Email — required, must be valid format
    password: str       # Plain text password — will be hashed before saving

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "name": "Sanya",
                    "email": "sanya@example.com",
                    "password": "mypassword123"
                }
            ]
        }
    }


# --- UserLogin ---
# Used when a user logs in (POST /auth/login)
class UserLogin(BaseModel):
    email: EmailStr     # Email to identify the user
    password: str       # Plain text password — will be verified against hash

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "email": "sanya@example.com",
                    "password": "mypassword123"
                }
            ]
        }
    }


# --- TokenResponse ---
# This is what the API returns after a successful login
class TokenResponse(BaseModel):
    access_token: str   # The JWT token the user will use for protected routes
    token_type: str     # Always "bearer"
