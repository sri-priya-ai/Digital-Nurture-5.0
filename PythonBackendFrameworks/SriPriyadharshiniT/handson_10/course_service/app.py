# course_service/app.py — Owns all department and course data.
# Runs on port 5001. Has its OWN database — no shared DB with student_service.
# The microservices rule: each service owns its data exclusively.

from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///courses_service.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Course(db.Model):
    id      = db.Column(db.Integer, primary_key=True)
    name    = db.Column(db.String(200), nullable=False)
    code    = db.Column(db.String(20),  unique=True)
    credits = db.Column(db.Integer)

    def to_dict(self):
        return {'id': self.id, 'name': self.name, 'code': self.code, 'credits': self.credits}


with app.app_context():
    db.create_all()


@app.route('/api/courses/', methods=['GET'])
def list_courses():
    return jsonify([c.to_dict() for c in Course.query.all()])


@app.route('/api/courses/', methods=['POST'])
def create_course():
    body = request.get_json()
    if not body:
        return jsonify({'error': 'JSON required'}), 400
    course = Course(name=body['name'], code=body['code'], credits=body.get('credits', 3))
    db.session.add(course); db.session.commit()
    return jsonify(course.to_dict()), 201


@app.route('/api/courses/<int:course_id>/', methods=['GET'])
def get_course(course_id):
    course = Course.query.get(course_id)
    if not course:
        return jsonify({'error': f'Course {course_id} not found'}), 404
    return jsonify(course.to_dict())


@app.route('/api/courses/<int:course_id>/', methods=['DELETE'])
def delete_course(course_id):
    course = Course.query.get(course_id)
    if not course:
        return jsonify({'error': 'Not found'}), 404
    db.session.delete(course); db.session.commit()
    return '', 204


if __name__ == '__main__':
    app.run(port=5001, debug=True)
