from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from database.connection import get_db
from database.user_models import UserTable
from auth.jwt_handler import verify_access_token

# This generates the Authorize button in Swagger
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    email = verify_access_token(token)
    if not email:
        raise HTTPException(status_code=401, detail="Invalid or expired token.")

    user = db.query(UserTable).filter(UserTable.email == email).first()
    if not user:
        raise HTTPException(status_code=401, detail="User not found.")

    return user