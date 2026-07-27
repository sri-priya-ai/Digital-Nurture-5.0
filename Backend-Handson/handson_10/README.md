# Hands-On 10 — Microservices Architecture: Concepts & Decomposition

## Services
| Service | Port | Owns |
|---|---|---|
| `course_service/` | 5001 | Course data, its own `course_service.db` |
| `student_service/` | 5002 | Student + Enrollment data, its own `student_service.db` |
| `gateway/` | 5000 | No data — proxies requests to the two services above |

## Bounded contexts (Step 96-97)
| Service | Responsibility | Endpoints it owns | Database it owns |
|---|---|---|---|
| Course Service | Department & course CRUD | `/api/courses/*` | `course_service.db` |
| Student Service | Student CRUD, enrollment | `/api/students/*` | `student_service.db` |
| Auth Service *(not built here — see Hands-On 9)* | Registration, login, token validation | `/api/v1/auth/*` | shared user store |
| Notification Service *(not built here — see Hands-On 7's background task)* | Email confirmations | — | — |

Only Course Service and Student Service are implemented as separate runnable
apps for this exercise, per the "start with 2 services" guidance in the hint.

## Setup — run each in its own terminal
```bash
# Terminal 1
cd course_service && pip install -r requirements.txt && python app.py

# Terminal 2
cd student_service && pip install -r requirements.txt && python app.py

# Terminal 3
cd gateway && pip install -r requirements.txt && python app.py
```

## Test through the gateway
```bash
curl http://localhost:5000/api/courses/
curl http://localhost:5000/api/students/
curl -X POST http://localhost:5000/api/students/1/enroll \
  -H "Content-Type: application/json" -d '{"course_id":1}'
```

Stop Course Service (Ctrl+C in Terminal 1) and repeat the enroll call —
Student Service catches the `ConnectionError` and the gateway returns
**503 Service Unavailable**.

## Synchronous vs asynchronous inter-service communication (Step 104)
- **Synchronous (HTTP, used here)**: simple to reason about and debug, but
  creates tight coupling — if Course Service is down, enrollment fails
  immediately.
- **Asynchronous (message queue, e.g. RabbitMQ/Kafka)**: Student Service
  would publish an "enrollment requested" event and continue immediately;
  Course Service (or a dedicated worker) consumes it later. This decouples
  the services and improves availability, at the cost of eventual
  consistency — the client no longer gets an instant yes/no answer, and
  the system needs a way to communicate delayed failures back to the user.
  A message queue is the better choice when the two services don't need to
  respond to the same request handshake in real time, or when you want the
  system to keep accepting enrollments even while a downstream service is
  temporarily unavailable.
