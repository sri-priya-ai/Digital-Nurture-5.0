# views.py — View functions for the courses app.
# Views are the controller layer in Django's MVT pattern.
# They receive a request, run any needed logic, and return a response.

from django.http import HttpResponse


def hello_view(request):
    """
    Basic health-check endpoint — confirms the server and routing
    are wired up correctly before we add models and real API logic.
    Returns plain text here; later views will return JSON.
    """
    return HttpResponse('Course Management API is running')
