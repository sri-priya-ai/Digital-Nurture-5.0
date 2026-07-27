# Hands-On 7 — FastAPI: Dependency Injection, CRUD & OpenAPI Documentation

## Setup
```bash
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload
```

Visit **http://127.0.0.1:8000/docs** for the interactive Swagger UI.

## What this covers
- Full CRUD for Departments, Courses, Students, Enrollments (SQLite + SQLAlchemy)
- `response_model` on GET/POST endpoints, correct status codes (201, 204, 404)
- `HTTPException` for consistent JSON error responses
- `GET /api/courses/{id}/students/` — JOIN query
- `BackgroundTasks` on `POST /api/enrollments/` — simulated confirmation email
- Custom OpenAPI metadata (title, description, version, contact) + endpoint tags

## Quick test
```bash
curl -X POST http://127.0.0.1:8000/api/departments/ -H "Content-Type: application/json" \
  -d '{"name":"Computer Science","budget":100000}'

curl -X POST http://127.0.0.1:8000/api/courses/ -H "Content-Type: application/json" \
  -d '{"name":"Intro to Python","code":"CS101","credits":4,"department_id":1}'
```
