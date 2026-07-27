# Python Backend Frameworks — Hands-On 7 to 10

Continues the Course Management API across Hands-On 1–6 (Django, Flask).
Hands-On 7, 8, and 9 continue the same FastAPI app built in Hands-On 6.
Hands-On 10 is a Flask microservices split (per the exercise book's note
that Hands-On 8–10 are framework-agnostic — pick one and continue).

## Hands-On 7 — FastAPI: Dependency Injection, CRUD & OpenAPI

```bash
cd handson_07
python -m venv venv && source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload
# Docs at http://127.0.0.1:8000/docs
```

## Hands-On 8 — RESTful API Design Best Practices

Same app, refactored: `/api/v1/` versioning, PATCH, Location headers,
pagination, search, standardised error format.

```bash
cd handson_08
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload
```

## Hands-On 9 — Authentication & Security: JWT, OAuth2 & OWASP

Adds bcrypt password hashing, JWT login, protected routes, CORS.

```bash
cd handson_09
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload
```

Register + login + call a protected route:
```bash
curl -X POST http://127.0.0.1:8000/api/v1/auth/register/ -H "Content-Type: application/json" \
  -d '{"email":"admin@example.com","password":"SuperSecret123"}'

TOKEN=$(curl -s -X POST http://127.0.0.1:8000/api/v1/auth/login/ -H "Content-Type: application/json" \
  -d '{"email":"admin@example.com","password":"SuperSecret123"}' | python3 -c "import json,sys;print(json.load(sys.stdin)['access_token'])")

curl -X POST http://127.0.0.1:8000/api/v1/courses/ -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" -d '{"name":"Intro","code":"CS101","credits":4,"department_id":1}'
```

## Hands-On 10 — Microservices: Course Service, Student Service, Gateway

Three separate Flask apps, each in its own subfolder, each with its own
`requirements.txt`. Run each in its own terminal:

```bash
# Terminal 1
cd handson_10/course_service
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
python app.py          # port 5001

# Terminal 2
cd handson_10/student_service
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
python app.py          # port 5002

# Terminal 3
cd handson_10/gateway
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
python app.py          # port 5000
```

Test through the gateway:
```bash
curl http://localhost:5000/api/courses/
curl -X POST http://localhost:5000/api/students/1/enroll \
  -H "Content-Type: application/json" -d '{"course_id":1}'
```

Stop `course_service` and repeat the enroll call to see the gateway
return `503 Service Unavailable`.

---

## Earlier hands-on (1–6), for reference

**Hands-On 1–3 (Django)**
```bash
cd handson_0X/coursemanager
pip install -r ../requirements.txt
python manage.py migrate
python manage.py runserver
```

**Hands-On 4 (Flask)**
```bash
cd handson_04/flask_coursemanager
pip install -r ../requirements.txt
python app.py
```

**Hands-On 5 (Flask + SQLAlchemy)**
```bash
cd handson_05/flask_coursemanager
pip install -r ../requirements.txt
flask db init && flask db migrate -m "initial" && flask db upgrade
python app.py
```

**Hands-On 6 (FastAPI)**
```bash
cd handson_06/fastapi_coursemanager
pip install -r ../requirements.txt
uvicorn main:app --reload
# Docs at http://127.0.0.1:8000/docs
```
