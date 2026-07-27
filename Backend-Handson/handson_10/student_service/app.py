"""
Student Service - handson_10
A standalone Flask microservice that owns Student and Enrollment data.
Runs on port 5002, with its own SQLite database.

The /enroll endpoint calls out to Course Service (port 5001) over HTTP
to verify the course exists before creating the enrollment - this
demonstrates synchronous inter-service communication (Step 100-101).

Run with:
    python app.py
"""

import requests
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///student_service.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

COURSE_SERVICE_URL = "http://127.0.0.1:5001"


class Student(db.Model):
    __tablename__ = "students"

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
        }


class Enrollment(db.Model):
    __tablename__ = "enrollments"

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey("students.id"), nullable=False)
    course_id = db.Column(db.Integer, nullable=False)  # owned by Course Service, not a local FK

    def to_dict(self):
        return {"id": self.id, "student_id": self.student_id, "course_id": self.course_id}


with app.app_context():
    db.create_all()
    if Student.query.count() == 0:
        db.session.add_all(
            [
                Student(first_name="Asha", last_name="Verma", email="asha@example.com"),
                Student(first_name="Rohan", last_name="Iyer", email="rohan@example.com"),
            ]
        )
        db.session.commit()


@app.errorhandler(404)
def not_found(_):
    return jsonify({"error": {"code": "NOT_FOUND", "message": "Resource not found"}}), 404


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok", "service": "student_service"})


@app.route("/api/students/", methods=["GET"])
def list_students():
    students = Student.query.all()
    return jsonify([s.to_dict() for s in students])


@app.route("/api/students/", methods=["POST"])
def create_student():
    data = request.get_json(silent=True)
    if not data or not all(k in data for k in ("first_name", "last_name", "email")):
        return jsonify({"error": {"code": "BAD_REQUEST", "message": "first_name, last_name, email required"}}), 400

    student = Student(first_name=data["first_name"], last_name=data["last_name"], email=data["email"])
    db.session.add(student)
    db.session.commit()
    return jsonify(student.to_dict()), 201


@app.route("/api/students/<int:student_id>/", methods=["GET"])
def get_student(student_id):
    student = db.session.get(Student, student_id)
    if student is None:
        return jsonify({"error": {"code": "NOT_FOUND", "message": "Student not found"}}), 404
    return jsonify(student.to_dict())


@app.route("/api/students/<int:student_id>/enroll", methods=["POST"])
def enroll_student(student_id):
    """
    Step 100-101: Verifies the course exists by calling Course Service.
    Returns 503 if Course Service is unreachable.
    """
    student = db.session.get(Student, student_id)
    if student is None:
        return jsonify({"error": {"code": "NOT_FOUND", "message": "Student not found"}}), 404

    data = request.get_json(silent=True) or {}
    course_id = data.get("course_id")
    if course_id is None:
        return jsonify({"error": {"code": "BAD_REQUEST", "message": "course_id required"}}), 400

    try:
        response = requests.get(f"{COURSE_SERVICE_URL}/api/courses/{course_id}/", timeout=3)
    except requests.exceptions.ConnectionError:
        return (
            jsonify(
                {
                    "error": {
                        "code": "SERVICE_UNAVAILABLE",
                        "message": "Course Service is currently unavailable. Please try again later.",
                    }
                }
            ),
            503,
        )

    if response.status_code == 404:
        return jsonify({"error": {"code": "NOT_FOUND", "message": "Course not found"}}), 404
    if response.status_code != 200:
        return jsonify({"error": {"code": "BAD_GATEWAY", "message": "Course Service returned an error"}}), 502

    enrollment = Enrollment(student_id=student_id, course_id=course_id)
    db.session.add(enrollment)
    db.session.commit()
    return jsonify(enrollment.to_dict()), 201


if __name__ == "__main__":
    app.run(port=5002, debug=True)
