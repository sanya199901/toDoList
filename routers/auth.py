from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm  # ← ADD THIS
from sqlalchemy.orm import Session

from models.user import UserRegister, TokenResponse
from database.user_models import UserTable
from database.connection import get_db
from passlib.context import CryptContext
from auth.jwt_handler import create_access_token

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(plain_password: str) -> str:
    return pwd_context.hash(plain_password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


# Register endpoint — same as before
@router.post("/register", summary="Register a new user")
def register(user: UserRegister, db: Session = Depends(get_db)):
    if len(user.password) < 6:
        raise HTTPException(status_code=400, detail="Password must be at least 6 characters")
    if len(user.password) > 72:
        raise HTTPException(status_code=400, detail="Password cannot be longer than 72 characters")

    existing_user = db.query(UserTable).filter(UserTable.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed = hash_password(user.password)
    new_user = UserTable(name=user.name, email=user.email, hashed_password=hashed)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {
        "message": "Account created successfully 🎉",
        "user": {"id": new_user.id, "name": new_user.name, "email": new_user.email}
    }


# ✅ Login now accepts form data — this makes Swagger Authorize button work!
@router.post("/login", response_model=TokenResponse, summary="Login and get token")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),  # ← reads username + password as form
    db: Session = Depends(get_db)
):
    # OAuth2PasswordRequestForm uses "username" field — we treat it as email
    db_user = db.query(UserTable).filter(UserTable.email == form_data.username).first()
    if not db_user or not verify_password(form_data.password, db_user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    token = create_access_token(data={"sub": db_user.email})
    return {"access_token": token, "token_type": "bearer"}