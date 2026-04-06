# FastAPI is our web framework
from fastapi import FastAPI

# Import database connection and Base (needed to create tables)
from database.connection import engine, Base

# Import our task router
from routers import tasks

# --- Create all tables in MySQL ---
# This looks at all classes that inherit from Base (like TaskTable)
# and creates the corresponding tables in MySQL if they don't exist yet
# ⚠️ Run this once — it won't delete existing data on restart
Base.metadata.create_all(bind=engine)

# --- Create the FastAPI app ---
app = FastAPI(
    title="Todo Task Manager API",
    description="Week 2 — Now with MySQL database! 🗄️",
    version="2.0.0"
)

# Register the tasks router
# All /tasks endpoints are now active
app.include_router(tasks.router)


# Root welcome endpoint
@app.get("/")
def root():
    return {
        "message": "Welcome to the Todo API 🚀",
        "week": "Week 2 — MySQL + Full CRUD",
        "docs": "Visit /docs for interactive API documentation"
    }
