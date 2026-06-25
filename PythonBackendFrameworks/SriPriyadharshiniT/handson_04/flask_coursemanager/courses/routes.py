# routes.py — Blueprint routes for the courses resource.
# A Blueprint groups related routes together — similar to Django apps
# but lighter. All routes here are mounted under /api/courses/.

from flask import Blueprint, jsonify, request

# url_prefix means every route in this blueprint starts with /api/courses
courses_bp = Blueprint('courses', __name__, url_prefix='/api/courses')

# Temporary in-memory store — replaced with a real DB in Hands-On 5
_courses = []
_next_id = 1


def make_envelope(data, status_code=200):
    """
    Wraps every response in a consistent JSON structure.
    Clients always know where to find data and whether the call succeeded.
    """
    return jsonify({'status': 'success', 'data': data}), status_code


@courses_bp.route('/', methods=['GET'])
def list_courses():
    """GET /api/courses/ — return every course"""
    return make_envelope(_courses)


@courses_bp.route('/', methods=['POST'])
def create_course():
    """POST /api/courses/ — create a new course from the request body"""
    global _next_id
    body = request.get_json()

    # Always check for None — get_json() returns None when Content-Type
    # header is not application/json
    if body is None:
        return jsonify({'status': 'error', 'message': 'Request body must be JSON'}), 400

    required = ['name', 'code', 'credits']
    missing  = [f for f in required if f not in body]
    if missing:
        return jsonify({
            'status': 'error',
            'message': f'Missing required fields: {", ".join(missing)}'
        }), 400

    course = {
        'id':      _next_id,
        'name':    body['name'],
        'code':    body['code'],
        'credits': body['credits'],
    }
    _courses.append(course)
    _next_id += 1
    return make_envelope(course, 201)


@courses_bp.route('/<int:course_id>/', methods=['GET'])
def get_course(course_id):
    """GET /api/courses/<id>/ — fetch one course by its ID"""
    course = next((c for c in _courses if c['id'] == course_id), None)
    if course is None:
        return jsonify({'status': 'error', 'message': f'Course {course_id} not found'}), 404
    return make_envelope(course)


@courses_bp.route('/<int:course_id>/', methods=['PUT'])
def update_course(course_id):
    """PUT /api/courses/<id>/ — replace all fields of an existing course"""
    course = next((c for c in _courses if c['id'] == course_id), None)
    if course is None:
        return jsonify({'status': 'error', 'message': f'Course {course_id} not found'}), 404

    body = request.get_json()
    if body is None:
        return jsonify({'status': 'error', 'message': 'Request body must be JSON'}), 400

    course.update({k: body[k] for k in ['name', 'code', 'credits'] if k in body})
    return make_envelope(course)


@courses_bp.route('/<int:course_id>/', methods=['DELETE'])
def delete_course(course_id):
    """DELETE /api/courses/<id>/ — remove a course permanently"""
    global _courses
    original_count = len(_courses)
    _courses = [c for c in _courses if c['id'] != course_id]
    if len(_courses) == original_count:
        return jsonify({'status': 'error', 'message': f'Course {course_id} not found'}), 404
    return '', 204
