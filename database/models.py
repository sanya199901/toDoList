# Column and types help us define what columns our database table has
from sqlalchemy import Column, Integer, String, Boolean
from database.connection import Base


# --- TaskTable ---
# This class represents the "tasks" table in your MySQL database
# Each attribute = one column in the table
class TaskTable(Base):

    # Name of the table in MySQL
    __tablename__ = "tasks"

    # Primary key — auto-increments for each new task (1, 2, 3...)
    id = Column(Integer, primary_key=True, index=True)

    # Task title — required, max 200 characters
    title = Column(String(200), nullable=False)

    # Task description — optional, max 500 characters
    description = Column(String(500), nullable=True)

    # Whether the task is done or not — defaults to False
    completed = Column(Boolean, default=False)
