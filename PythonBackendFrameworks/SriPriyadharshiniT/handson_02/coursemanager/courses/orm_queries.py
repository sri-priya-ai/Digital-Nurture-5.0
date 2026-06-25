# orm_queries.py — Sample ORM queries for Task 2.
# Run these inside the Django shell: python manage.py shell
# then: from courses.orm_queries import *  (or paste manually)

# This file is for reference — it won't run standalone because
# it needs the Django app registry to be initialised first.

"""
STEP 1 — Create sample data
----------------------------
from courses.models import Department, Course, Student, Enrollment

cs   = Department.objects.create(name='Computer Science', head_of_dept='Dr. Smith', budget=500000)
math = Department.objects.create(name='Mathematics', head_of_dept='Dr. Patel', budget=300000)

c1 = Course.objects.create(name='Intro to Python', code='CS101', credits=3, department=cs)
c2 = Course.objects.create(name='Data Structures', code='CS201', credits=4, department=cs)
c3 = Course.objects.create(name='Linear Algebra', code='MA101', credits=3, department=math)
c4 = Course.objects.create(name='Web Development', code='CS301', credits=3, department=cs)

s1 = Student.objects.create(first_name='Alice', last_name='Johnson', email='alice@college.edu', department=cs, enrollment_year=2023)
s2 = Student.objects.create(first_name='Bob', last_name='Kumar', email='bob@college.edu', department=math, enrollment_year=2022)
s3 = Student.objects.create(first_name='Carol', last_name='Lee', email='carol@college.edu', department=cs, enrollment_year=2024)
s4 = Student.objects.create(first_name='David', last_name='Nair', email='david@college.edu', department=cs, enrollment_year=2023)
s5 = Student.objects.create(first_name='Eva', last_name='Ramos', email='eva@college.edu', department=math, enrollment_year=2024)


STEP 2 — Filter courses by department (double underscore = JOIN)
-----------------------------------------------------------------
cs_courses = Course.objects.filter(department__name='Computer Science')
for c in cs_courses:
    print(c.name)
# The __ traverses the ForeignKey relationship — Django builds the JOIN for you


STEP 3 — Count courses per department using annotate
------------------------------------------------------
from django.db.models import Count

dept_counts = Department.objects.annotate(course_count=Count('courses'))
for d in dept_counts:
    print(f'{d.name}: {d.course_count} courses')


STEP 4 — select_related to avoid N+1 queries
---------------------------------------------
from django.db import connection

# Without select_related — hits DB once per student to get department
students = Student.objects.all()
for s in students:
    print(s.department.name)  # separate query each time!

# With select_related — single JOIN query fetches everything at once
students = Student.objects.select_related('department').all()
for s in students:
    print(s.department.name)  # no extra queries

# Check query count
print(len(connection.queries))


STEP 5 — Bulk update using F() expression
------------------------------------------
from django.db.models import F

# F() lets you reference a field value inside the DB itself.
# The multiplication happens in SQL — no Python round-trip.
Department.objects.update(budget=F('budget') * 1.1)
# Confirm the update
for d in Department.objects.all():
    print(d.name, d.budget)
"""
