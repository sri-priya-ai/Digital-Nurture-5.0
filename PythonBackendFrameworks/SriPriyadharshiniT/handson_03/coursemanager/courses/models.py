# models.py — Core data models for the Course Management system.
# Each class maps to a database table. Django's ORM handles all the
# SQL — we just write Python and let the migrations do the rest.

from django.db import models


class Department(models.Model):
    # Stores faculty/department info. Courses and students belong to a dept.
    name         = models.CharField(max_length=120)
    head_of_dept = models.CharField(max_length=120)
    budget       = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    def __str__(self):
        # This string shows up in the admin and shell repr
        return self.name


class Course(models.Model):
    name       = models.CharField(max_length=200)
    code       = models.CharField(max_length=20, unique=True)  # e.g. CS101
    credits    = models.PositiveIntegerField()
    # CASCADE means deleting a Department also removes all its courses.
    # Think carefully — in some systems you'd use PROTECT instead.
    department = models.ForeignKey(
        Department, on_delete=models.CASCADE, related_name='courses'
    )

    def __str__(self):
        return f'{self.code} — {self.name}'


class Student(models.Model):
    first_name      = models.CharField(max_length=80)
    last_name       = models.CharField(max_length=80)
    email           = models.EmailField(unique=True)
    department      = models.ForeignKey(
        Department, on_delete=models.SET_NULL, null=True, related_name='students'
    )
    enrollment_year = models.PositiveIntegerField()

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class Enrollment(models.Model):
    student         = models.ForeignKey(Student, on_delete=models.CASCADE)
    course          = models.ForeignKey(Course, on_delete=models.CASCADE)
    enrollment_date = models.DateField(auto_now_add=True)
    # Grade is nullable — a student may not have a grade yet
    grade           = models.CharField(max_length=5, null=True, blank=True)

    class Meta:
        # Prevents the same student from enrolling in the same course twice
        unique_together = [['student', 'course']]

    def __str__(self):
        return f'{self.student} → {self.course}'
