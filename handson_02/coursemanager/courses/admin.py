from django.contrib import admin
from .models import Department, Course, Student, Enrollment


@admin.register(Department)
class DeptAdmin(admin.ModelAdmin):
    list_display = ['dept_name', 'dept_head', 'annual_budget']
    search_fields = ['dept_name']


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['course_title', 'course_code', 'credit_hours', 'dept']
    search_fields = ['course_title', 'course_code']
    list_filter = ['dept']


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['fname', 'lname', 'email_addr', 'join_year']
    search_fields = ['fname', 'lname', 'email_addr']


@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ['student', 'course', 'enrolled_on', 'grade_val']
    list_filter = ['course']
