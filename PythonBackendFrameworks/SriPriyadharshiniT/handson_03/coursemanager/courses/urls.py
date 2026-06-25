# courses/urls.py — Uses DRF's DefaultRouter to auto-generate all URL patterns.
# Registering a ViewSet with the router creates both the list and detail URLs
# automatically — no need to write them one by one.

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register('departments', views.DepartmentViewSet, basename='department')
router.register('courses',     views.CourseViewSet,     basename='course')
router.register('students',    views.StudentViewSet,    basename='student')
router.register('enrollments', views.EnrollmentViewSet, basename='enrollment')

# router.urls expands to all the patterns above automatically
urlpatterns = [
    path('', include(router.urls)),
]
