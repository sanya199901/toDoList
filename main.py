from fastapi import FastAPI
from fastapi.security import HTTPBearer

from database.connection import engine, Base
from database.models import TaskTable
from database.user_models import UserTable
from routers import tasks
from routers import auth

Base.metadata.create_all(bind=engine)

# ✅ This adds the Bearer token field in Swagger Authorize popup
security = HTTPBearer()

app = FastAPI(
    title="Todo Task Manager API",
    description="Week 4 — Tasks linked to users 🔐",
    version="4.0.0"
)

app.include_router(auth.router)
app.include_router(tasks.router)

@app.get("/")
def root():
    return {
        "message": "Welcome to the Todo API 🚀",
        "docs": "Visit /docs for interactive API documentation"
    }