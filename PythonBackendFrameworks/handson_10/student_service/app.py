import requests
from flask import Flask, jsonify, request

svc = Flask(__name__)

COURSE_SVC = 'http://localhost:5001'

student_store = [
    {'stu_id': 1, 'fname': 'Arun', 'lname': 'Kumar', 'email_addr': 'arun@college.edu'},
    {'stu_id': 2, 'fname': 'Priya', 'lname': 'Sharma', 'email_addr': 'priya@college.edu'},
]
enroll_store = []
nxt_sid = 3


@svc.route('/api/students/', methods=['GET'])
def all_students():
    return jsonify(student_store)


@svc.route('/api/students/<int:sid>/', methods=['GET'])
def single_student(sid):
    match = next((s for s in student_store if s['stu_id'] == sid), None)
    if not match:
        return jsonify({'error': 'Student not found'}), 404
    return jsonify(match)


@svc.route('/api/students/', methods=['POST'])
def add_student():
    global nxt_sid
    body = request.get_json()
    if not body:
        return jsonify({'error': 'JSON required'}), 400
    entry = {
        'stu_id': nxt_sid,
        'fname': body.get('fname', ''),
        'lname': body.get('lname', ''),
        'email_addr': body.get('email_addr', ''),
    }
    student_store.append(entry)
    nxt_sid += 1
    return jsonify(entry), 201


@svc.route('/api/students/<int:sid>/enroll', methods=['POST'])
def enroll_student(sid):
    stu = next((s for s in student_store if s['stu_id'] == sid), None)
    if not stu:
        return jsonify({'error': 'Student not found'}), 404

    body = request.get_json()
    cid = body.get('course_id') if body else None
    if not cid:
        return jsonify({'error': 'course_id required'}), 400

    # call course service to verify the course exists
    try:
        resp = requests.get(f'{COURSE_SVC}/api/courses/{cid}/', timeout=3)
    except requests.exceptions.ConnectionError:
        return jsonify({'error': 'Course service unavailable'}), 503

    if resp.status_code == 404:
        return jsonify({'error': f'Course {cid} not found'}), 404

    record = {'stu_id': sid, 'course_id': cid}
    enroll_store.append(record)
    return jsonify({'message': 'Enrolled', 'enrollment': record}), 201


@svc.route('/api/students/<int:sid>/enrollments/', methods=['GET'])
def student_enrollments(sid):
    mine = [e for e in enroll_store if e['stu_id'] == sid]
    return jsonify(mine)


if __name__ == '__main__':
    svc.run(port=5002, debug=True)
