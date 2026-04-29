# SQLAlchemy setup — now reads credentials from .env via config.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

# Import settings from config.py instead of hardcoding credentials
from config import settings

# Build the database URL from .env variables
# No more hardcoded passwords! ✅
DATABASE_URL = (
    f"mysql+pymysql://{settings.DB_USER}:{settings.DB_PASSWORD}"
    f"@{settings.DB_HOST}/{settings.DB_NAME}"
)

# Engine — actual connection to MySQL
engine = create_engine(DATABASE_URL)

# Session — one per request, closed after
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Base class — all table models inherit from this
class Base(DeclarativeBase):
    pass


# Dependency — gives each endpoint a fresh DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
