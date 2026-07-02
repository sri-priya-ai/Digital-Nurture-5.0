from django.db import models


class Department(models.Model):
    dept_name = models.CharField(max_length=150)
    dept_head = models.CharField(max_length=100)
    annual_budget = models.DecimalField(max_digits=12, decimal_places=2)

    def __str__(self):
        return self.dept_name


class Course(models.Model):
    course_title = models.CharField(max_length=200)
    course_code = models.CharField(max_length=20, unique=True)
    credit_hours = models.IntegerField()
    dept = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='courses')

    def __str__(self):
        return self.course_title


class Student(models.Model):
    fname = models.CharField(max_length=80)
    lname = models.CharField(max_length=80)
    email_addr = models.EmailField(unique=True)
    dept = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, related_name='students')
    join_year = models.IntegerField()

    def __str__(self):
        return f"{self.fname} {self.lname}"


class Enrollment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='enrollments')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='enrollments')
    enrolled_on = models.DateField(auto_now_add=True)
    grade_val = models.CharField(max_length=5, blank=True, null=True)

    class Meta:
        unique_together = [['student', 'course']]

    def __str__(self):
        return f"{self.student} -> {self.course}"
