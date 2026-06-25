# gateway/app.py — Simple API Gateway that proxies requests to the right service.
# Runs on port 5000 (the single entry point clients talk to).
# In production an API gateway also handles auth, rate limiting,
# SSL termination, and load balancing — this version just does routing.

import requests
from flask import Flask, jsonify, request, Response

app = Flask(__name__)

COURSE_SERVICE  = 'http://localhost:5001'
STUDENT_SERVICE = 'http://localhost:5002'


def proxy(service_url, path):
    """
    Forwards the incoming request to the appropriate service and
    streams the response back. Preserves method, headers, and body.
    """
    target_url = f'{service_url}{path}'
    try:
        resp = requests.request(
            method  = request.method,
            url     = target_url,
            headers = {k: v for k, v in request.headers if k != 'Host'},
            json    = request.get_json(silent=True),
            timeout = 10,
        )
        return Response(resp.content, status=resp.status_code,
                        content_type=resp.headers.get('Content-Type', 'application/json'))
    except requests.ConnectionError:
        return jsonify({'error': f'Service at {service_url} is unreachable'}), 503


@app.route('/api/courses/', defaults={'path': '/api/courses/'}, methods=['GET', 'POST'])
@app.route('/api/courses/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def route_courses(path):
    """All /api/courses/* requests → course_service (port 5001)"""
    full_path = f'/api/courses/{path}' if not path.startswith('/') else path
    return proxy(COURSE_SERVICE, full_path)


@app.route('/api/students/', defaults={'path': '/api/students/'}, methods=['GET', 'POST'])
@app.route('/api/students/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def route_students(path):
    """All /api/students/* requests → student_service (port 5002)"""
    full_path = f'/api/students/{path}' if not path.startswith('/') else path
    return proxy(STUDENT_SERVICE, full_path)


if __name__ == '__main__':
    app.run(port=5000, debug=True)
