# Hands-On 9 — Authentication & Security: JWT, OAuth2 & OWASP

## Setup
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload
```

## What this covers (built on top of Hands-On 8)
- `security.py`: `get_password_hash()` / `verify_password()` using passlib + bcrypt
- `POST /api/v1/auth/register/` — hashes the password, returns 409 on duplicate email
- `POST /api/v1/auth/login/` — verifies credentials, returns a JWT (`{access_token, token_type}`)
- `get_current_user` dependency — decodes/validates the JWT, raises 401 if invalid/expired
- `POST /api/v1/courses/`, `PATCH /api/v1/courses/{id}`, `DELETE /api/v1/courses/{id}` are
  **protected** (require `Authorization: Bearer <token>`); `GET` endpoints remain public
- CORS configured for `http://localhost:3000`

## Quick test
```bash
# Register
curl -X POST http://127.0.0.1:8000/api/v1/auth/register/ -H "Content-Type: application/json" \
  -d '{"email":"admin@example.com","password":"SuperSecret123"}'

# Login
TOKEN=$(curl -s -X POST http://127.0.0.1:8000/api/v1/auth/login/ -H "Content-Type: application/json" \
  -d '{"email":"admin@example.com","password":"SuperSecret123"}' | python3 -c "import json,sys;print(json.load(sys.stdin)['access_token'])")

# Use the token on a protected route
curl -X POST http://127.0.0.1:8000/api/v1/courses/ -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" -d '{"name":"Intro","code":"CS101","credits":4,"department_id":1}'
```

## Note on secrets
`security.py` has a hard-coded `SECRET_KEY` for local development only. In any real deployment,
load it from an environment variable (`os.environ["JWT_SECRET_KEY"]`) and never commit it to Git.
