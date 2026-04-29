from fastapi import FastAPI
from database.connection import engine, Base
from database.models import TaskTable
from database.user_models import UserTable
from routers import tasks, auth

# Auto-create all tables in MySQL on startup
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Todo Task Manager API",
    description="""
## 🚀 Todo Task Manager API

A production-ready REST API built with **FastAPI** and **MySQL**.

### Features
- ✅ User registration and login
- 🔐 JWT authentication
- 📝 Full CRUD for tasks
- 👤 Each user sees only their own tasks
- 📄 Auto-generated Swagger documentation

### How to use
1. Register a new account via `/auth/register`
2. Login via `/auth/login`
3. Click **Authorize** and enter your credentials
4. Start managing your tasks!
    """,
    version="5.0.0"
)

app.include_router(auth.router)
app.include_router(tasks.router)


@app.get("/", tags=["Root"])
def root():
    return {
        "message": "Welcome to the Todo Task Manager API 🚀",
        "docs": "Visit /docs for interactive API documentation",
        "version": "5.0.0"
    }
