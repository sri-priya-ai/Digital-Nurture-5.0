# student_service/app.py — Owns all student and enrollment data.
# Runs on port 5002. Has its OWN database (students_service.db).
# To enroll a student, this service calls course_service to verify
# the course exists — demonstrating synchronous inter-service communication.

import requests
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///students_service.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# The address of course_service — in production this would come from
# a service registry or environment variable, not a hardcoded string
COURSE_SERVICE_URL = 'http://localhost:5001'


class Student(db.Model):
    id         = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(80))
    last_name  = db.Column(db.String(80))
    email      = db.Column(db.String(200), unique=True)

    def to_dict(self):
        return {'id': self.id, 'first_name': self.first_name,
                'last_name': self.last_name, 'email': self.email}


class Enrollment(db.Model):
    id        = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'))
    course_id  = db.Column(db.Integer, nullable=False)  # foreign key to a different service!


with app.app_context():
    db.create_all()


@app.route('/api/students/', methods=['GET'])
def list_students():
    return jsonify([s.to_dict() for s in Student.query.all()])


@app.route('/api/students/', methods=['POST'])
def create_student():
    body = request.get_json()
    if not body:
        return jsonify({'error': 'JSON required'}), 400
    student = Student(
        first_name=body['first_name'],
        last_name=body['last_name'],
        email=body['email']
    )
    db.session.add(student); db.session.commit()
    return jsonify(student.to_dict()), 201


@app.route('/api/students/<int:student_id>/enroll', methods=['POST'])
def enroll_student(student_id):
    """
    Enrolls a student in a course.
    Before creating the enrollment, this service calls course_service
    to verify the course actually exists — cross-service validation.

    The downside: if course_service is down, enrollment is impossible.
    This is the tight-coupling trade-off of synchronous HTTP calls.
    A message queue (RabbitMQ/Kafka) would decouple this at the cost
    of eventual consistency.
    """
    student = Student.query.get(student_id)
    if not student:
        return jsonify({'error': f'Student {student_id} not found'}), 404

    body      = request.get_json()
    course_id = body.get('course_id')

    # Verify the course exists in course_service
    try:
        resp = requests.get(f'{COURSE_SERVICE_URL}/api/courses/{course_id}/', timeout=5)
    except requests.ConnectionError:
        # Course service is unreachable — return 503 Service Unavailable
        return jsonify({'error': 'Course service is unavailable. Try again later.'}), 503

    if resp.status_code == 404:
        return jsonify({'error': f'Course {course_id} does not exist'}), 404

    enrollment = Enrollment(student_id=student_id, course_id=course_id)
    db.session.add(enrollment); db.session.commit()
    return jsonify({'enrollment_id': enrollment.id, 'student_id': student_id, 'course_id': course_id}), 201


if __name__ == '__main__':
    app.run(port=5002, debug=True)
