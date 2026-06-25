# views.py — Hands-On 9: JWT authentication + protected endpoints.
# Builds on HO8 — adds registration, login, and route protection.

from django.http import JsonResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.db import IntegrityError

from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed

from jose import JWTError

from .models import Department, Course, Student, Enrollment, User
from .serializers import (
    DepartmentSerializer, CourseSerializer,
    StudentSerializer, EnrollmentSerializer,
)
from .security import get_password_hash, verify_password, create_access_token, decode_access_token


# ── Custom JWT Authentication for DRF ────────────────────────────
class JWTAuthentication(BaseAuthentication):
    """
    DRF authentication class that reads a Bearer token from the
    Authorization header and looks up the corresponding user.
    Plugs into DRF's permission system — no extra middleware needed.
    """
    def authenticate(self, request):
        auth_header = request.headers.get('Authorization', '')
        if not auth_header.startswith('Bearer '):
            return None  # No token — let DRF handle as anonymous

        token = auth_header.split(' ')[1]
        try:
            payload = decode_access_token(token)
            user    = User.objects.get(email=payload['sub'])
            return (user, token)
        except (JWTError, User.DoesNotExist):
            raise AuthenticationFailed('Token is invalid or expired')


# ── Auth Views ────────────────────────────────────────────────────
@method_decorator(csrf_exempt, name='dispatch')
class RegisterView(View):
    def post(self, request):
        import json
        body = json.loads(request.body)
        email    = body.get('email', '').strip()
        password = body.get('password', '')

        if not email or not password:
            return JsonResponse({'error': {'code': 'MISSING_FIELDS', 'message': 'Email and password required'}}, status=400)

        try:
            user = User.objects.create(
                email=email,
                hashed_password=get_password_hash(password)
            )
            return JsonResponse({'id': user.id, 'email': user.email}, status=201)
        except IntegrityError:
            # 409 Conflict — email already registered
            return JsonResponse({'error': {'code': 'CONFLICT', 'message': 'Email already registered'}}, status=409)


@method_decorator(csrf_exempt, name='dispatch')
class LoginView(View):
    def post(self, request):
        import json
        body     = json.loads(request.body)
        email    = body.get('email', '')
        password = body.get('password', '')

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return JsonResponse({'error': {'code': 'UNAUTHORISED', 'message': 'Invalid credentials'}}, status=401)

        if not verify_password(password, user.hashed_password):
            return JsonResponse({'error': {'code': 'UNAUTHORISED', 'message': 'Invalid credentials'}}, status=401)

        token = create_access_token({'sub': user.email})
        return JsonResponse({'access_token': token, 'token_type': 'bearer'})


# ── Course ViewSet with auth on write operations ──────────────────
class CourseViewSet(viewsets.ModelViewSet):
    queryset         = Course.objects.select_related('department').all()
    serializer_class = CourseSerializer
    # Our custom JWT auth class — DRF checks this on every request
    authentication_classes = [JWTAuthentication]

    def get_permissions(self):
        """
        Read operations (GET) are open to everyone.
        Write operations (POST, PUT, PATCH, DELETE) require a valid JWT.
        This is a common pattern: public read, authenticated write.
        """
        if self.action in ('list', 'retrieve'):
            return [AllowAny()]
        return [IsAuthenticated()]

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response({'error': {'code': 'VALIDATION_ERROR', 'message': str(serializer.errors)}}, status=400)
        course  = serializer.save()
        headers = {'Location': f'/api/v1/courses/{course.id}/'}
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def destroy(self, request, pk=None):
        try:
            course = Course.objects.get(pk=pk)
        except Course.DoesNotExist:
            return Response({'error': {'code': 'NOT_FOUND', 'message': f'Course {pk} not found'}}, status=404)
        course.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class StudentViewSet(viewsets.ModelViewSet):
    queryset               = Student.objects.all()
    serializer_class       = StudentSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes     = [IsAuthenticated]


class EnrollmentViewSet(viewsets.ModelViewSet):
    queryset               = Enrollment.objects.all()
    serializer_class       = EnrollmentSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes     = [IsAuthenticated]
