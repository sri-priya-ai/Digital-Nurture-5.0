from flask import Flask, jsonify, request

svc = Flask(__name__)

dept_store = [
    {'dept_id': 1, 'dept_name': 'Computer Science'},
    {'dept_id': 2, 'dept_name': 'Mathematics'},
]

course_store = [
    {'course_id': 1, 'course_title': 'Data Structures', 'course_code': 'CS101', 'dept_id': 1},
    {'course_id': 2, 'course_title': 'Algorithms', 'course_code': 'CS102', 'dept_id': 1},
    {'course_id': 3, 'course_title': 'Calculus', 'course_code': 'MA101', 'dept_id': 2},
]
nxt_cid = 4


@svc.route('/api/courses/', methods=['GET'])
def all_courses():
    return jsonify(course_store)


@svc.route('/api/courses/<int:cid>/', methods=['GET'])
def single_course(cid):
    match = next((c for c in course_store if c['course_id'] == cid), None)
    if not match:
        return jsonify({'error': 'Course not found'}), 404
    return jsonify(match)


@svc.route('/api/courses/', methods=['POST'])
def add_course():
    global nxt_cid
    body = request.get_json()
    if not body:
        return jsonify({'error': 'JSON required'}), 400
    entry = {
        'course_id': nxt_cid,
        'course_title': body.get('course_title', ''),
        'course_code': body.get('course_code', ''),
        'dept_id': body.get('dept_id', 1),
    }
    course_store.append(entry)
    nxt_cid += 1
    return jsonify(entry), 201


@svc.route('/api/departments/', methods=['GET'])
def all_depts():
    return jsonify(dept_store)


if __name__ == '__main__':
    svc.run(port=5001, debug=True)
