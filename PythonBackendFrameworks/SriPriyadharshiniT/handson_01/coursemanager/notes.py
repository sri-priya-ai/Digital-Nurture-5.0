# ================================================================
# Hands-On 1 — Task 1: Framework Concepts & Request Lifecycle
# ================================================================

# ── 1. GET /api/courses/ journey through Django ──────────────────
# 1. Browser sends HTTP GET /api/courses/
# 2. WSGI server (dev: runserver, prod: gunicorn) receives raw HTTP
#    and wraps it into Django's HttpRequest object
# 3. Middleware stack runs top-to-bottom — security checks,
#    session loading, CSRF validation, user injection
# 4. URL router matches /api/courses/ to the correct view function
# 5. View runs — queries Model layer (Course.objects.all())
# 6. ORM converts that call into SQL, hits the database
# 7. DB returns rows → ORM turns them into Python objects
# 8. View serialises data into JSON and returns HttpResponse
# 9. Middleware runs bottom-to-top on the way out (adds headers etc.)
# 10. Response travels back to the browser

# ── 2. Middleware position & two built-in examples ───────────────
# Middleware wraps the view like layers of an onion.
# It sees EVERY request before the view and EVERY response after.

# SecurityMiddleware — adds HTTPS redirect, sets security headers
# like X-Content-Type-Options and X-XSS-Protection, prevents
# browsers from sniffing MIME types and running clickjacking attacks.

# SessionMiddleware — reads the session cookie on each request,
# loads the session data into request.session so any view can use it,
# then saves changes back to the session store on the way out.

# ── 3. WSGI vs ASGI ──────────────────────────────────────────────
# WSGI — synchronous standard (PEP 3333). One request is fully
# handled before the next one starts inside that worker process.
# Django uses WSGI by default. Perfectly fine for most web apps.

# ASGI — asynchronous standard. Supports async/await views,
# WebSockets, and long-lived connections. Django ships with asgi.py
# but does NOT enable it by default.

# Switch to ASGI when you need:
#   - WebSockets (live chat, real-time dashboards)
#   - async def views to avoid blocking I/O
#   - High concurrency with many simultaneous connections

# ── 4. MVC → Django MVT mapping ──────────────────────────────────
# Classic MVC:   Model | View (presentation) | Controller (logic)
# Django MVT:    Model | Template (presentation) | View (logic)
#
# Django's "View"     = MVC's Controller  → handles request logic
# Django's "Template" = MVC's View        → renders the output
# Django's "Model"    = MVC's Model       → same, talks to the DB
#
# The naming is intentionally different — Django's "View" is NOT
# the presentation layer. Once you internalise this the whole
# framework structure makes sense.
