from flask import Blueprint, jsonify, request

courses_bp = Blueprint('courses', __name__, url_prefix='/api/courses')

# In-memory store for testing before DB integration
course_store = []
next_id = 1


def build_resp(payload, code=200):
    return jsonify({'status': 'success', 'data': payload}), code


@courses_bp.route('/', methods=['GET'])
def list_courses():
    return build_resp(course_store)


@courses_bp.route('/', methods=['POST'])
def add_course():
    global next_id
    body = request.get_json()
    if not body:
        return jsonify({'error': 'Request body must be JSON'}), 400

    missing = [f for f in ('name', 'code', 'credits') if f not in body]
    if missing:
        return jsonify({'error': f"Missing fields: {', '.join(missing)}"}), 400

    new_entry = {
        'id': next_id,
        'name': body['name'],
        'code': body['code'],
        'credits': body['credits'],
    }
    course_store.append(new_entry)
    next_id += 1
    return build_resp(new_entry, 201)


@courses_bp.route('/<int:cid>/', methods=['GET'])
def fetch_course(cid):
    match = next((c for c in course_store if c['id'] == cid), None)
    if not match:
        return jsonify({'error': f'Course {cid} not found'}), 404
    return build_resp(match)


@courses_bp.route('/<int:cid>/', methods=['PUT'])
def modify_course(cid):
    match = next((c for c in course_store if c['id'] == cid), None)
    if not match:
        return jsonify({'error': f'Course {cid} not found'}), 404

    body = request.get_json()
    if not body:
        return jsonify({'error': 'Request body must be JSON'}), 400

    match.update({k: body[k] for k in ('name', 'code', 'credits') if k in body})
    return build_resp(match)


@courses_bp.route('/<int:cid>/', methods=['DELETE'])
def remove_course(cid):
    global course_store
    idx = next((i for i, c in enumerate(course_store) if c['id'] == cid), None)
    if idx is None:
        return jsonify({'error': f'Course {cid} not found'}), 404
    course_store.pop(idx)
    return '', 204
