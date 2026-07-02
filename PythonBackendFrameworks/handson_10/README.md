# Handson 10 — Microservices Architecture

## Service Decomposition

| Service Name       | Responsibility                        | Endpoints Owned                                       | Database          |
|--------------------|---------------------------------------|-------------------------------------------------------|-------------------|
| Course Service     | Department and course CRUD            | /api/courses/, /api/departments/                      | courses.db        |
| Student Service    | Student CRUD and enrollment           | /api/students/, /api/students/{id}/enroll             | students.db       |
| Auth Service       | Registration, login, token validation | /api/auth/register/, /api/auth/login/                 | auth.db           |
| Notification Svc   | Email confirmations, alerts           | Internal only (consumes events from other services)   | notifications.db  |

## Running the Services

```bash
# Terminal 1 — Course Service (port 5001)
cd course_service && python app.py

# Terminal 2 — Student Service (port 5002)
cd student_service && python app.py

# Terminal 3 — API Gateway (port 5000)
cd gateway && python app.py
```

## Test the Full Flow

```bash
# Enroll student 1 in course 2 via gateway
curl -X POST http://localhost:5000/api/students/1/enroll \
  -H "Content-Type: application/json" \
  -d '{"course_id": 2}'
```

Stop the Course Service and repeat the call — Student Service returns 503.

## Synchronous vs Asynchronous Inter-Service Communication

**Synchronous (HTTP — what we built):**
- Simple to implement and reason about
- Student Service is tightly coupled to Course Service — if Course Service goes down, enrollment fails
- Works well for low-latency operations where the client needs an immediate answer

**Asynchronous (Message Queue — RabbitMQ / Kafka):**
- Student Service publishes an "enroll" event to a queue; Course Service consumes it independently
- Services are decoupled — if Course Service is temporarily down, messages queue up and process when it recovers
- Results in eventual consistency — the enrollment may not be confirmed instantly
- Better for high-throughput pipelines, notifications, and audit logs
- Use a message queue when: you don't need a real-time answer, services have very different uptime requirements,
  or you need to fan out one event to multiple consumers (e.g. send email AND update analytics)
