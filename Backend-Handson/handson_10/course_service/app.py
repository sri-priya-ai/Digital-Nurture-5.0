"""
Course Service - handson_10
A standalone Flask microservice that owns Course data only.
Runs on port 5001, with its own SQLite database.

Run with:
    python app.py
"""

from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///course_service.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


class Course(db.Model):
    __tablename__ = "courses"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    code = db.Column(db.String(20), unique=True, nullable=False)
    credits = db.Column(db.Integer, nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "code": self.code,
            "credits": self.credits,
        }


with app.app_context():
    db.create_all()
    # Seed a couple of courses so the service is useful out of the box
    if Course.query.count() == 0:
        db.session.add_all(
            [
                Course(name="Intro to Python", code="CS101", credits=4),
                Course(name="Data Structures", code="CS102", credits=4),
            ]
        )
        db.session.commit()


@app.errorhandler(404)
def not_found(_):
    return jsonify({"error": {"code": "NOT_FOUND", "message": "Resource not found"}}), 404


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok", "service": "course_service"})


@app.route("/api/courses/", methods=["GET"])
def list_courses():
    courses = Course.query.all()
    return jsonify([c.to_dict() for c in courses])


@app.route("/api/courses/", methods=["POST"])
def create_course():
    data = request.get_json(silent=True)
    if not data or not all(k in data for k in ("name", "code", "credits")):
        return jsonify({"error": {"code": "BAD_REQUEST", "message": "name, code, credits required"}}), 400

    course = Course(name=data["name"], code=data["code"], credits=data["credits"])
    db.session.add(course)
    db.session.commit()
    return jsonify(course.to_dict()), 201


@app.route("/api/courses/<int:course_id>/", methods=["GET"])
def get_course(course_id):
    course = db.session.get(Course, course_id)
    if course is None:
        return jsonify({"error": {"code": "NOT_FOUND", "message": "Course not found"}}), 404
    return jsonify(course.to_dict())


@app.route("/api/courses/<int:course_id>/", methods=["DELETE"])
def delete_course(course_id):
    course = db.session.get(Course, course_id)
    if course is None:
        return jsonify({"error": {"code": "NOT_FOUND", "message": "Course not found"}}), 404
    db.session.delete(course)
    db.session.commit()
    return "", 204


if __name__ == "__main__":
    app.run(port=5001, debug=True)
