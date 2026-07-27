"""
API Gateway - handson_10
A minimal Flask app that proxies incoming requests to the correct
backend microservice based on the URL path.

    /api/courses/*  -> Course Service  (http://127.0.0.1:5001)
    /api/students/* -> Student Service (http://127.0.0.1:5002)

Run with:
    python app.py
Then everything is accessible through port 5000, e.g.:
    POST http://localhost:5000/api/students/1/enroll
"""

import requests
from flask import Flask, request, Response

app = Flask(__name__)

SERVICE_ROUTES = {
    "courses": "http://127.0.0.1:5001",
    "students": "http://127.0.0.1:5002",
}

# Headers that should not be forwarded as-is between hops
HOP_BY_HOP_HEADERS = {
    "content-length",
    "connection",
    "keep-alive",
    "transfer-encoding",
    "host",
}


@app.route("/health", methods=["GET"])
def health():
    return {"status": "ok", "service": "api_gateway"}


@app.route("/api/<resource>/", defaults={"path": ""}, methods=["GET", "POST", "PUT", "PATCH", "DELETE"])
@app.route("/api/<resource>/<path:path>", methods=["GET", "POST", "PUT", "PATCH", "DELETE"])
def proxy(resource, path):
    """
    Step 102: Routes /api/courses/* to Course Service and
    /api/students/* to Student Service using requests.request().
    """
    base_url = SERVICE_ROUTES.get(resource)
    if base_url is None:
        return {"error": {"code": "NOT_FOUND", "message": f"No service registered for '{resource}'"}}, 404

    target_url = f"{base_url}/api/{resource}/{path}"

    forward_headers = {k: v for k, v in request.headers if k.lower() not in HOP_BY_HOP_HEADERS}

    try:
        upstream_response = requests.request(
            method=request.method,
            url=target_url,
            headers=forward_headers,
            params=request.args,
            data=request.get_data(),
            timeout=5,
        )
    except requests.exceptions.ConnectionError:
        return (
            {"error": {"code": "SERVICE_UNAVAILABLE", "message": f"{resource} service is unavailable"}},
            503,
        )

    excluded_headers = HOP_BY_HOP_HEADERS
    response_headers = [
        (name, value) for name, value in upstream_response.raw.headers.items()
        if name.lower() not in excluded_headers
    ]

    return Response(upstream_response.content, upstream_response.status_code, response_headers)


if __name__ == "__main__":
    app.run(port=5000, debug=True)
