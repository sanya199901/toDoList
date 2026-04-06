# SQLAlchemy is the ORM (Object Relational Mapper) we use to talk to MySQL
# Instead of writing raw SQL, we write Python and SQLAlchemy translates it
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

# --- Database Connection URL ---
# Format: mysql+pymysql://<username>:<password>@<host>/<database_name>
# ⚠️ Change "root" and "your_password" to match your MySQL Workbench credentials
DATABASE_URL = "mysql+pymysql://root:your_new_password@localhost/todo_db"

# --- Engine ---
# The engine is the actual connection to your MySQL database
engine = create_engine(DATABASE_URL)

# --- Session ---
# A session is like a "conversation" with the database
# Every request gets its own session, and we close it when done
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# --- Base Class ---
# All our database table models will inherit from this Base class
class Base(DeclarativeBase):
    pass


# --- Dependency ---
# This function is used in our endpoints to get a DB session
# It automatically closes the session after the request is done
def get_db():
    db = SessionLocal()
    try:
        yield db  # Give the session to the endpoint
    finally:
        db.close()  # Always close after use
