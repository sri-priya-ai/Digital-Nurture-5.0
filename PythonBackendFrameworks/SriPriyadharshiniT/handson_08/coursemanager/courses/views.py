# views.py — Hands-On 8: REST best practices applied.
# Changes from HO3: versioned URLs, PATCH support, Location header on POST,
# standardised error format, and offset pagination with envelope response.

from django.db.models import Q
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Department, Course, Student, Enrollment
from .serializers import (
    DepartmentSerializer, CourseSerializer,
    StudentSerializer, EnrollmentSerializer,
)


def error_response(code, message, field=None, http_status=400):
    """
    Every error in this API follows the same JSON structure:
    { error: { code, message, field } }
    Consistent error shapes make it much easier for frontend teams to handle
    errors generically instead of guessing the format per endpoint.
    """
    return Response(
        {'error': {'code': code, 'message': message, 'field': field}},
        status=http_status
    )


class CourseViewSet(viewsets.ModelViewSet):
    serializer_class = CourseSerializer

    def get_queryset(self):
        qs     = Course.objects.select_related('department').all()
        search = self.request.query_params.get('search', '')
        if search:
            # Case-insensitive search across both name and course code
            qs = qs.filter(Q(name__icontains=search) | Q(code__icontains=search))
        return qs

    def list(self, request):
        """
        GET /api/v1/courses/?page=1&page_size=5&search=python
        Returns a paginated envelope matching the DRF pagination standard:
        { count, next, previous, results }
        Clients use count + page_size to build pagination controls.
        """
        page      = int(request.query_params.get('page', 1))
        page_size = int(request.query_params.get('page_size', 10))
        qs        = self.get_queryset()
        total     = qs.count()
        start     = (page - 1) * page_size
        end       = start + page_size
        results   = qs[start:end]

        base_url = request.build_absolute_uri(request.path)
        next_url = f'{base_url}?page={page+1}&page_size={page_size}' if end < total else None
        prev_url = f'{base_url}?page={page-1}&page_size={page_size}' if page > 1 else None

        serializer = self.get_serializer(results, many=True)
        return Response({
            'count':    total,
            'next':     next_url,
            'previous': prev_url,
            'results':  serializer.data,
        })

    def create(self, request):
        """POST /api/v1/courses/ — returns 201 + Location header pointing to new resource"""
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return error_response('VALIDATION_ERROR', 'Invalid data', http_status=400)
        course = serializer.save()
        headers = {'Location': f'/api/v1/courses/{course.id}/'}
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def retrieve(self, request, pk=None):
        try:
            course = Course.objects.get(pk=pk)
        except Course.DoesNotExist:
            return error_response('NOT_FOUND', f'Course with id {pk} does not exist', http_status=404)
        return Response(self.get_serializer(course).data)

    def partial_update(self, request, pk=None):
        """PATCH /api/v1/courses/{id}/ — update only the supplied fields"""
        try:
            course = Course.objects.get(pk=pk)
        except Course.DoesNotExist:
            return error_response('NOT_FOUND', f'Course with id {pk} does not exist', http_status=404)
        serializer = self.get_serializer(course, data=request.data, partial=True)
        if not serializer.is_valid():
            return error_response('VALIDATION_ERROR', str(serializer.errors), http_status=400)
        serializer.save()
        return Response(serializer.data)

    def destroy(self, request, pk=None):
        try:
            course = Course.objects.get(pk=pk)
        except Course.DoesNotExist:
            return error_response('NOT_FOUND', f'Course with id {pk} does not exist', http_status=404)
        course.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=['get'])
    def students(self, request, pk=None):
        try:
            course = Course.objects.get(pk=pk)
        except Course.DoesNotExist:
            return error_response('NOT_FOUND', f'Course {pk} not found', http_status=404)
        enrollments = Enrollment.objects.filter(course=course).select_related('student')
        students    = [e.student for e in enrollments]
        return Response(StudentSerializer(students, many=True).data)


class StudentViewSet(viewsets.ModelViewSet):
    queryset         = Student.objects.select_related('department').all()
    serializer_class = StudentSerializer


class EnrollmentViewSet(viewsets.ModelViewSet):
    queryset         = Enrollment.objects.select_related('student', 'course').all()
    serializer_class = EnrollmentSerializer
