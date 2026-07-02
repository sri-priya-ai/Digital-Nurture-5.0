from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, viewsets
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404

from .models import Course, Student, Enrollment
from .serializers import CourseSerializer, StudentSerializer, EnrollmentSerializer


class CourseListView(APIView):
    def get(self, req):
        all_courses = Course.objects.all()
        sr = CourseSerializer(all_courses, many=True)
        return Response(sr.data)

    def post(self, req):
        sr = CourseSerializer(data=req.data)
        if sr.is_valid():
            sr.save()
            return Response(sr.data, status=status.HTTP_201_CREATED)
        return Response(sr.errors, status=status.HTTP_400_BAD_REQUEST)


class CourseDetailView(APIView):
    def get_obj(self, pk):
        return get_object_or_404(Course, pk=pk)

    def get(self, req, pk):
        obj = self.get_obj(pk)
        sr = CourseSerializer(obj)
        return Response(sr.data)

    def put(self, req, pk):
        obj = self.get_obj(pk)
        sr = CourseSerializer(obj, data=req.data)
        if sr.is_valid():
            sr.save()
            return Response(sr.data)
        return Response(sr.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, req, pk):
        obj = self.get_obj(pk)
        obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    @action(detail=True, methods=['get'], url_path='students')
    def enrolled_students(self, req, pk=None):
        course_obj = self.get_object()
        enrolled = Enrollment.objects.filter(course=course_obj).select_related('student')
        student_list = [e.student for e in enrolled]
        sr = StudentSerializer(student_list, many=True)
        return Response(sr.data)


class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer


class EnrollmentViewSet(viewsets.ModelViewSet):
    queryset = Enrollment.objects.all()
    serializer_class = EnrollmentSerializer
