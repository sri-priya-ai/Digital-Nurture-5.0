import requests
from flask import Flask, jsonify, request, Response

gw = Flask(__name__)

COURSE_SVC = 'http://localhost:5001'
STUDENT_SVC = 'http://localhost:5002'


def proxy(target_url):
    try:
        resp = requests.request(
            method=request.method,
            url=target_url,
            headers={k: v for k, v in request.headers if k != 'Host'},
            data=request.get_data(),
            params=request.args,
            timeout=5,
        )
        return Response(resp.content, status=resp.status_code, content_type=resp.headers.get('Content-Type'))
    except requests.exceptions.ConnectionError:
        return jsonify({'error': 'Upstream service unavailable'}), 503


@gw.route('/api/courses/', defaults={'tail': ''}, methods=['GET', 'POST'])
@gw.route('/api/courses/<path:tail>', methods=['GET', 'POST', 'PUT', 'PATCH', 'DELETE'])
def fwd_courses(tail):
    dest = f'{COURSE_SVC}/api/courses/{tail}'
    return proxy(dest)


@gw.route('/api/students/', defaults={'tail': ''}, methods=['GET', 'POST'])
@gw.route('/api/students/<path:tail>', methods=['GET', 'POST', 'PUT', 'PATCH', 'DELETE'])
def fwd_students(tail):
    dest = f'{STUDENT_SVC}/api/students/{tail}'
    return proxy(dest)


if __name__ == '__main__':
    gw.run(port=5000, debug=True)
