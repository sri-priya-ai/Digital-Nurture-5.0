# admin.py — Registers models with Django's built-in admin panel.
# The admin gives full CRUD on all models with almost zero code.
# We customise it here to make it more useful day-to-day.

from django.contrib import admin
from .models import Department, Course, Student, Enrollment


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display  = ['name', 'head_of_dept', 'budget']
    search_fields = ['name', 'head_of_dept']


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    # list_display controls the columns shown in the course list page
    list_display  = ['name', 'code', 'credits', 'department']
    # search_fields enables the search bar — searches these columns
    search_fields = ['name', 'code']
    # list_filter adds a sidebar filter — click to narrow by department
    list_filter   = ['department']


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display  = ['first_name', 'last_name', 'email', 'department', 'enrollment_year']
    search_fields = ['first_name', 'last_name', 'email']
    list_filter   = ['department', 'enrollment_year']


@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ['student', 'course', 'enrollment_date', 'grade']
    list_filter  = ['course']
