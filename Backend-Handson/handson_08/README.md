# Hands-On 8 — RESTful API Design Best Practices

## Setup
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload
```

## What this covers (built on top of Hands-On 7)
- **Versioning**: all routes moved to `/api/v1/...`
- **PATCH vs PUT**: `PUT /api/v1/courses/{id}` requires the full resource;
  `PATCH /api/v1/courses/{id}` updates only the supplied fields
- **Location header**: every `POST` returns a `Location` header pointing to
  the new resource
- **Pagination**: `GET /api/v1/courses/?page=1&page_size=2` returns a
  DRF-style envelope: `{count, next, previous, results}`
- **Filtering**: `GET /api/v1/courses/?search=data` — case-insensitive
  match on course name or code
- **Standardised errors**: every error response follows
  `{"error": {"code": "NOT_FOUND", "message": "...", "field": null}}`
  via a global `HTTPException` handler

## Quick test
```bash
curl "http://127.0.0.1:8000/api/v1/courses/?page=1&page_size=2"
curl -X PATCH http://127.0.0.1:8000/api/v1/courses/1 -H "Content-Type: application/json" -d '{"credits":5}'
```
