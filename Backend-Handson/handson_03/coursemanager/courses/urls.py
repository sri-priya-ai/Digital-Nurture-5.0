from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

rtr = DefaultRouter()
rtr.register('courses', views.CourseViewSet)
rtr.register('students', views.StudentViewSet)
rtr.register('enrollments', views.EnrollmentViewSet)

urlpatterns = [
    path('', include(rtr.urls)),
]
