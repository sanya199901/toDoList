# BaseModel from Pydantic — used for request body validation
from pydantic import BaseModel


# --- Task ---
# Used when CREATING a task (request body)
# This is what the user sends to the API
class Task(BaseModel):
    title: str              # Required
    description: str = ""   # Optional — defaults to empty string
    completed: bool = False # Optional — defaults to False

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "title": "Buy groceries",
                    "description": "Milk, eggs, and bread",
                    "completed": False
                }
            ]
        }
    }


# --- TaskUpdate ---
# Used when UPDATING a task (all fields are optional)
# This way user can update just the title, or just completed, etc.
class TaskUpdate(BaseModel):
    title: str | None = None              # Optional update
    description: str | None = None        # Optional update
    completed: bool | None = None         # Optional update

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "title": "Buy groceries and fruits",
                    "completed": True
                }
            ]
        }
    }
