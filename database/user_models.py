# Column types for defining table structure
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from database.connection import Base


# --- UserTable ---
# Updated this week — users now have a list of tasks
class UserTable(Base):

    __tablename__ = "users"

    # Primary key — auto-increments
    id = Column(Integer, primary_key=True, index=True)

    # User's full name — required
    name = Column(String(100), nullable=False)

    # User's email — required and unique
    email = Column(String(100), nullable=False, unique=True)

    # Hashed password — never plain text
    hashed_password = Column(String(255), nullable=False)

    # ✅ NEW THIS WEEK — Relationship to TaskTable
    # This lets us access user.tasks to get all tasks belonging to this user
    # cascade="all, delete" means deleting user deletes their tasks too
    tasks = relationship("TaskTable", back_populates="owner", cascade="all, delete")
