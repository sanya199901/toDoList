# 📝 Todo Task Manager API

A production-ready **REST API** built with **FastAPI** and **MySQL** — developed as part of a 5-week LinkedIn series on building real-world backend applications with Python.

---

## 🚀 Features

- ✅ User registration and login
- 🔐 JWT authentication (Bearer tokens)
- 📝 Full CRUD operations for tasks
- 👤 Each user can only access their own tasks
- 🗄️ MySQL database with SQLAlchemy ORM
- 📄 Auto-generated Swagger UI documentation

---

## 🗂️ Project Structure

```
todo-api/
│
├── main.py                    ← App entry point
├── config.py                  ← Loads environment variables
├── requirements.txt           ← All dependencies
├── .env.example               ← Environment variables template
├── .gitignore
│
├── auth/
│   ├── jwt_handler.py         ← Create & verify JWT tokens
│   └── dependencies.py        ← get_current_user dependency
│
├── database/
│   ├── connection.py          ← MySQL connection setup
│   ├── models.py              ← Tasks table definition
│   └── user_models.py         ← Users table definition
│
├── routers/
│   ├── auth.py                ← Register & Login endpoints
│   └── tasks.py               ← CRUD task endpoints
│
└── models/
    ├── task.py                ← Task Pydantic models
    └── user.py                ← User Pydantic models
```

---

## ⚙️ Setup & Installation

### 1. Clone the repository
```bash
git clone https://github.com/sanya199901/toDoList.git
cd toDoList
```

### 2. Create and activate virtual environment
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Set up MySQL database
- Open **MySQL Workbench**
- Create a new schema named `todo_db`

### 5. Create your `.env` file
```bash
# Copy the example file
cp .env.example .env
```

Then open `.env` and fill in your credentials:
```
DB_USER=root
DB_PASSWORD=your_mysql_password
DB_HOST=localhost
DB_NAME=todo_db
SECRET_KEY=your_secret_key_here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### 6. Run the application
```bash
uvicorn main:app --reload
```

### 7. Open API docs
```
http://127.0.0.1:8000/docs
```

---

## 📌 API Endpoints

### Authentication
| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/auth/register` | Create a new account | ❌ |
| POST | `/auth/login` | Login and get JWT token | ❌ |

### Tasks
| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/tasks/` | Get all my tasks | ✅ |
| GET | `/tasks/{id}` | Get a single task | ✅ |
| POST | `/tasks/` | Create a new task | ✅ |
| PUT | `/tasks/{id}` | Update a task | ✅ |
| DELETE | `/tasks/{id}` | Delete a task | ✅ |

---

## 🔐 How Authentication Works

1. Register via `POST /auth/register`
2. Login via `POST /auth/login` → get a JWT token
3. Click **Authorize** in Swagger UI
4. Enter your email and password
5. All protected endpoints are now accessible ✅

---

## 🛠️ Tech Stack

| Technology | Purpose |
|------------|---------|
| **FastAPI** | Web framework |
| **MySQL** | Database |
| **SQLAlchemy** | ORM |
| **PyMySQL** | MySQL driver |
| **Pydantic** | Data validation |
| **JWT (python-jose)** | Authentication tokens |
| **bcrypt (passlib)** | Password hashing |
| **Uvicorn** | ASGI server |

---

## 📚 LinkedIn Series

This project was built as part of a 5-week public learning series:

| Week | Topic |
|------|-------|
| Week 1 | FastAPI intro + first endpoint |
| Week 2 | MySQL + Full CRUD |
| Week 3 | User registration + JWT auth |
| Week 4 | Tasks linked to users |
| Week 5 | Final polish + GitHub release |

---

## 👩‍💻 Author

**Sanya Tare**
[LinkedIn](https://www.linkedin.com/in/sanya-tare-85b583194)
[GitHub](https://github.com/sanya199901)
