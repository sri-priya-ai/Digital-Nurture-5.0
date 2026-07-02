"""
Run these inside: python manage.py shell
"""

from courses.models import Department, Course, Student, Enrollment
from django.db.models import Count, F


def seed_data():
    d1 = Department.objects.create(dept_name='Computer Science', dept_head='Dr. Rao', annual_budget=500000)
    d2 = Department.objects.create(dept_name='Mathematics', dept_head='Dr. Patel', annual_budget=300000)

    Course.objects.create(course_title='Data Structures', course_code='CS101', credit_hours=4, dept=d1)
    Course.objects.create(course_title='Algorithms', course_code='CS102', credit_hours=4, dept=d1)
    Course.objects.create(course_title='Calculus', course_code='MA101', credit_hours=3, dept=d2)
    Course.objects.create(course_title='Linear Algebra', course_code='MA102', credit_hours=3, dept=d2)

    for i in range(1, 6):
        Student.objects.create(
            fname=f'Student{i}',
            lname=f'Last{i}',
            email_addr=f'stu{i}@college.edu',
            dept=d1,
            join_year=2023
        )


def run_queries():
    cs_courses = Course.objects.filter(dept__dept_name='Computer Science')
    print("CS courses:", list(cs_courses))

    dept_counts = Department.objects.annotate(num_courses=Count('courses'))
    for d in dept_counts:
        print(d.dept_name, d.num_courses)

    students_with_dept = Student.objects.select_related('dept').all()
    for s in students_with_dept:
        print(s.fname, s.dept.dept_name)

    Department.objects.update(annual_budget=F('annual_budget') * 1.1)
    print("Budgets updated by 10%")
