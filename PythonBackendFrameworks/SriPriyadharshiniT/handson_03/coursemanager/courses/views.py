# views.py — API views for the Course Management system.
# We use DRF ViewSets which bundle all CRUD operations in one class,
# and a custom action to fetch students enrolled in a specific course.

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Department, Course, Student, Enrollment
from .serializers import (
    DepartmentSerializer, CourseSerializer,
    StudentSerializer, EnrollmentSerializer,
)


class DepartmentViewSet(viewsets.ModelViewSet):
    """
    ModelViewSet automatically provides:
    GET    /api/departments/        → list all
    POST   /api/departments/        → create one
    GET    /api/departments/{pk}/   → retrieve one
    PUT    /api/departments/{pk}/   → full update
    PATCH  /api/departments/{pk}/   → partial update
    DELETE /api/departments/{pk}/   → delete
    """
    queryset         = Department.objects.all()
    serializer_class = DepartmentSerializer


class CourseViewSet(viewsets.ModelViewSet):
    queryset         = Course.objects.select_related('department').all()
    serializer_class = CourseSerializer

    @action(detail=True, methods=['get'], url_path='students')
    def enrolled_students(self, request, pk=None):
        """
        Custom action: GET /api/courses/{pk}/students/
        Returns all students currently enrolled in this course.
        The @action decorator registers this as an extra endpoint
        outside the standard CRUD pattern.
        """
        course = self.get_object()
        # Traverse Enrollment → Student to get the enrolled student objects
        enrollments = Enrollment.objects.filter(course=course).select_related('student')
        students    = [e.student for e in enrollments]
        serializer  = StudentSerializer(students, many=True)
        return Response(serializer.data)


class StudentViewSet(viewsets.ModelViewSet):
    queryset         = Student.objects.select_related('department').all()
    serializer_class = StudentSerializer


class EnrollmentViewSet(viewsets.ModelViewSet):
    queryset         = Enrollment.objects.select_related('student', 'course').all()
    serializer_class = EnrollmentSerializer
