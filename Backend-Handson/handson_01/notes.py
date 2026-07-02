# Request-Response Cycle in Django for GET /api/courses/
#
# 1. Browser sends HTTP GET to /api/courses/
# 2. Django's URL router (urls.py) matches the path and finds the view
# 3. Middleware stack runs (e.g. SecurityMiddleware, SessionMiddleware)
# 4. The matched view function/class executes
# 5. View queries the database via Model (ORM)
# 6. Model returns queryset/data to the view
# 7. View serializes and wraps data into an HttpResponse / JsonResponse
# 8. Middleware runs again on the way out (response phase)
# 9. Response travels back to the browser

# Middleware sits between the URL dispatcher and the view.
# It wraps each request/response — think of it as a pipeline of plugins.
#
# Two built-in Django middleware classes:
#
# SecurityMiddleware:
#   Adds security-related HTTP headers (e.g. X-Content-Type-Options, HSTS).
#   Redirects HTTP to HTTPS when SECURE_SSL_REDIRECT is True.
#
# SessionMiddleware:
#   Reads the session cookie from the incoming request and loads
#   the session data so views can access request.session.


# WSGI vs ASGI
#
# WSGI (Web Server Gateway Interface):
#   Synchronous protocol. Each request is handled one at a time per worker.
#   Django uses WSGI by default (wsgi.py).
#   Works well for traditional request/response APIs.
#
# ASGI (Asynchronous Server Gateway Interface):
#   Supports async views, WebSockets, and long-lived connections.
#   Switch to ASGI when you need real-time features (chat, live updates)
#   or want to write async def views for high-concurrency workloads.
#   Django supports ASGI via asgi.py — run with uvicorn or daphne.


# MVC vs Django MVT
#
# Classic MVC:
#   Model     — data and business logic
#   View      — what the user sees (presentation layer)
#   Controller — handles input, coordinates model and view
#
# Django MVT:
#   Model     — same as MVC Model (data, ORM)
#   Template  — equivalent to MVC View (HTML/JSON rendering)
#   View      — equivalent to MVC Controller (processes request, calls model, returns response)
#
# The naming difference trips people up. Django's "View" is really the controller.
