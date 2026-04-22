# APIRouter groups all task endpoints together
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

# Pydantic models for request validation
from models.task import Task, TaskUpdate

# Database table model
from database.models import TaskTable

# DB session dependency
from database.connection import get_db

# ✅ NEW THIS WEEK — gets the currently logged in user from JWT token
from auth.dependencies import get_current_user

# UserTable needed for type hinting the current user
from database.user_models import UserTable

router = APIRouter(
    prefix="/tasks",
    tags=["Tasks"]
)


# --- GET /tasks/ ---
# ✅ PROTECTED — only logged in users can access
# Returns ONLY the tasks belonging to the logged in user
@router.get("/", summary="Get my tasks")
def get_tasks(
    db: Session = Depends(get_db),
    current_user: UserTable = Depends(get_current_user)  # ← reads JWT token
):
    # Filter tasks by the logged in user's ID
    # So user A can never see user B's tasks
    tasks = db.query(TaskTable).filter(TaskTable.user_id == current_user.id).all()
    return {
        "user": current_user.name,
        "tasks": tasks,
        "total": len(tasks)
    }


# --- GET /tasks/{task_id} ---
# ✅ PROTECTED — returns a single task only if it belongs to the logged in user
@router.get("/{task_id}", summary="Get a single task")
def get_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: UserTable = Depends(get_current_user)
):
    # Find task by ID AND user_id — prevents accessing other users' tasks
    task = db.query(TaskTable).filter(
        TaskTable.id == task_id,
        TaskTable.user_id == current_user.id
    ).first()

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    return task


# --- POST /tasks/ ---
# ✅ PROTECTED — creates a task and links it to the logged in user
@router.post("/", summary="Create a new task")
def create_task(
    task: Task,
    db: Session = Depends(get_db),
    current_user: UserTable = Depends(get_current_user)
):
    new_task = TaskTable(
        title=task.title,
        description=task.description,
        completed=task.completed,
        user_id=current_user.id   # ← link task to the logged in user
    )

    db.add(new_task)
    db.commit()
    db.refresh(new_task)

    return {"message": "Task created successfully ✅", "task": new_task}


# --- PUT /tasks/{task_id} ---
# ✅ PROTECTED — updates a task only if it belongs to the logged in user
@router.put("/{task_id}", summary="Update a task")
def update_task(
    task_id: int,
    updated: TaskUpdate,
    db: Session = Depends(get_db),
    current_user: UserTable = Depends(get_current_user)
):
    # Find task by ID AND verify it belongs to the logged in user
    task = db.query(TaskTable).filter(
        TaskTable.id == task_id,
        TaskTable.user_id == current_user.id
    ).first()

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    # Only update fields that were actually sent
    if updated.title is not None:
        task.title = updated.title
    if updated.description is not None:
        task.description = updated.description
    if updated.completed is not None:
        task.completed = updated.completed

    db.commit()
    db.refresh(task)

    return {"message": "Task updated successfully ✏️", "task": task}


# --- DELETE /tasks/{task_id} ---
# ✅ PROTECTED — deletes a task only if it belongs to the logged in user
@router.delete("/{task_id}", summary="Delete a task")
def delete_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: UserTable = Depends(get_current_user)
):
    # Find task by ID AND verify ownership
    task = db.query(TaskTable).filter(
        TaskTable.id == task_id,
        TaskTable.user_id == current_user.id
    ).first()

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    db.delete(task)
    db.commit()

    return {"message": f"Task '{task.title}' deleted successfully 🗑️"}
