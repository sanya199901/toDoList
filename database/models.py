# Column types for defining table structure
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from database.connection import Base


# --- TaskTable ---
# Updated this week — tasks now have an owner (user)
class TaskTable(Base):

    __tablename__ = "tasks"

    # Primary key — auto-increments
    id = Column(Integer, primary_key=True, index=True)

    # Task title — required
    title = Column(String(200), nullable=False)

    # Task description — optional
    description = Column(String(500), nullable=True)

    # Whether task is done — defaults to False
    completed = Column(Boolean, default=False)

    # ✅ NEW THIS WEEK — Foreign key linking task to a user
    # This means every task MUST belong to a user
    # ondelete="CASCADE" means if user is deleted, their tasks are deleted too
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    # ✅ NEW THIS WEEK — Relationship to UserTable
    # This lets us access task.owner.name, task.owner.email etc.
    owner = relationship("UserTable", back_populates="tasks")
