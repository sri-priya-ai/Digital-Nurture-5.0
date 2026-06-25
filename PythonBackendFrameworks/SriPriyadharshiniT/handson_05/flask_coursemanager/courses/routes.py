# routes.py — Course routes backed by SQLAlchemy instead of in-memory list.
# The logic is identical to Hands-On 4 except every operation now
# hits the real database through the ORM.

from flask import Blueprint, jsonify, request
from app import db
from .models import Course, Enrollment, Student

courses_bp = Blueprint('courses', __name__, url_prefix='/api/courses')


@courses_bp.route('/', methods=['GET'])
def list_courses():
    courses = Course.query.all()
    return jsonify({'status': 'success', 'data': [c.to_dict() for c in courses]})


@courses_bp.route('/', methods=['POST'])
def create_course():
    body = request.get_json()
    if not body:
        return jsonify({'status': 'error', 'message': 'JSON body required'}), 400

    missing = [f for f in ['name', 'code', 'credits', 'department_id'] if f not in body]
    if missing:
        return jsonify({'status': 'error', 'message': f'Missing: {missing}'}), 400

    course = Course(
        name=body['name'], code=body['code'],
        credits=body['credits'], department_id=body['department_id']
    )
    db.session.add(course)
    db.session.commit()
    return jsonify({'status': 'success', 'data': course.to_dict()}), 201


@courses_bp.route('/<int:course_id>/', methods=['GET'])
def get_course(course_id):
    # get_or_404 does the primary-key lookup AND the 404 abort in one call
    course = Course.query.get_or_404(course_id)
    return jsonify({'status': 'success', 'data': course.to_dict()})


@courses_bp.route('/<int:course_id>/', methods=['PUT'])
def update_course(course_id):
    course = Course.query.get_or_404(course_id)
    body   = request.get_json()
    if not body:
        return jsonify({'status': 'error', 'message': 'JSON body required'}), 400

    for field in ['name', 'code', 'credits', 'department_id']:
        if field in body:
            setattr(course, field, body[field])
    db.session.commit()
    return jsonify({'status': 'success', 'data': course.to_dict()})


@courses_bp.route('/<int:course_id>/', methods=['DELETE'])
def delete_course(course_id):
    course = Course.query.get_or_404(course_id)
    db.session.delete(course)
    db.session.commit()
    return '', 204


@courses_bp.route('/<int:course_id>/students/', methods=['GET'])
def enrolled_students(course_id):
    """Returns all students currently enrolled in this course via a JOIN"""
    course = Course.query.get_or_404(course_id)
    students = (
        Student.query
        .join(Enrollment, Enrollment.student_id == Student.id)
        .filter(Enrollment.course_id == course.id)
        .all()
    )
    return jsonify({'status': 'success', 'data': [s.to_dict() for s in students]})
