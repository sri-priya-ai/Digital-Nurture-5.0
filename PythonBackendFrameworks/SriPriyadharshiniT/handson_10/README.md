# Hands-On 10 — Microservices Architecture

## Services

| Service         | Port | Database               | Owns                        |
|-----------------|------|------------------------|-----------------------------|
| gateway         | 5000 | none                   | Routing only                |
| course_service  | 5001 | courses_service.db     | Courses                     |
| student_service | 5002 | students_service.db    | Students + Enrollments      |

## How to run

Open 3 separate terminals:

```bash
# Terminal 1 — Course Service
cd course_service && python app.py

# Terminal 2 — Student Service
cd student_service && python app.py

# Terminal 3 — Gateway
cd gateway && python app.py
```

## Test the full flow

```bash
# Create a course (via gateway → course_service)
POST http://localhost:5000/api/courses/
{ "name": "Python Basics", "code": "CS101", "credits": 3 }

# Create a student (via gateway → student_service)
POST http://localhost:5000/api/students/
{ "first_name": "Alice", "last_name": "Smith", "email": "alice@college.edu" }

# Enroll the student — student_service calls course_service internally
POST http://localhost:5002/api/students/1/enroll
{ "course_id": 1 }

# Stop course_service, try enrollment again — should get 503
```

## Sync vs Async inter-service communication

**Synchronous (HTTP — used here)**
- Simple to implement and debug
- Creates tight coupling — if course_service is down, enrollment fails
- Fine for low-traffic, non-critical workflows

**Asynchronous (message queue — RabbitMQ, Kafka)**
- Student service publishes an "EnrollmentRequested" event to a queue
- Course service consumes it and validates/confirms asynchronously
- Services are decoupled — course_service going down doesn't block enrollment
- Trade-off: eventual consistency — the student may not see confirmation instantly
- Use this when: high throughput, fault tolerance, or the operation is non-critical
