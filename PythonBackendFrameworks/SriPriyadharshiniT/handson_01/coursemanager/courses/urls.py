# courses/urls.py — URL patterns for the courses app.
# Keeping URL config inside the app (not in the project's urls.py)
# makes each app self-contained and easy to plug into any project.

from django.urls import path
from . import views

urlpatterns = [
    # GET /api/hello/ → hello_view — sanity check endpoint
    path('hello/', views.hello_view, name='hello'),
]
