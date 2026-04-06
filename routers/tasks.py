# APIRouter groups all task-related endpoints together
from fastapi import APIRouter, Depends, HTTPException

# Session is used for type hinting the DB session
from sqlalchemy.orm import Session

# Our Pydantic models for request validation
from models.task import Task, TaskUpdate

# The database table model
from database.models import TaskTable

# get_db gives us a database session for each request
from database.connection import get_db

# Create router — all routes will start with /tasks
router = APIRouter(
    prefix="/tasks",
    tags=["Tasks"]
)


# --- GET /tasks/ ---
# Fetch all tasks from the MySQL database
@router.get("/", summary="Get all tasks")
def get_tasks(db: Session = Depends(get_db)):
    # Query the tasks table and return all rows
    tasks = db.query(TaskTable).all()
    return {"tasks": tasks, "total": len(tasks)}


# --- GET /tasks/{task_id} ---
# Fetch a single task by its ID
@router.get("/{task_id}", summary="Get a task by ID")
def get_task(task_id: int, db: Session = Depends(get_db)):
    # Look for task with matching ID
    task = db.query(TaskTable).filter(TaskTable.id == task_id).first()

    # If not found, return a 404 error
    if not task:
        raise HTTPException(status_code=404, detail=f"Task with id {task_id} not found")

    return task


# --- POST /tasks/ ---
# Create a new task and save it to MySQL
@router.post("/", summary="Create a new task")
def create_task(task: Task, db: Session = Depends(get_db)):
    # Create a new TaskTable object (this maps to a row in the DB)
    new_task = TaskTable(
        title=task.title,
        description=task.description,
        completed=task.completed
    )

    db.add(new_task)       # Stage the new task for saving
    db.commit()            # Actually save it to MySQL
    db.refresh(new_task)   # Refresh to get the auto-generated ID back

    return {"message": "Task created successfully ✅", "task": new_task}


# --- PUT /tasks/{task_id} ---
# Update an existing task by ID
@router.put("/{task_id}", summary="Update a task")
def update_task(task_id: int, updated: TaskUpdate, db: Session = Depends(get_db)):
    # Find the task to update
    task = db.query(TaskTable).filter(TaskTable.id == task_id).first()

    # If not found, return 404
    if not task:
        raise HTTPException(status_code=404, detail=f"Task with id {task_id} not found")

    # Only update fields that were actually sent in the request
    # (None means the user didn't send that field — skip it)
    if updated.title is not None:
        task.title = updated.title

    if updated.description is not None:
        task.description = updated.description

    if updated.completed is not None:
        task.completed = updated.completed

    db.commit()         # Save changes to MySQL
    db.refresh(task)    # Refresh to get latest data

    return {"message": "Task updated successfully ✏️", "task": task}


# --- DELETE /tasks/{task_id} ---
# Delete a task by ID
@router.delete("/{task_id}", summary="Delete a task")
def delete_task(task_id: int, db: Session = Depends(get_db)):
    # Find the task to delete
    task = db.query(TaskTable).filter(TaskTable.id == task_id).first()

    # If not found, return 404
    if not task:
        raise HTTPException(status_code=404, detail=f"Task with id {task_id} not found")

    db.delete(task)   # Mark for deletion
    db.commit()       # Execute deletion in MySQL

    return {"message": f"Task '{task.title}' deleted successfully 🗑️"}
