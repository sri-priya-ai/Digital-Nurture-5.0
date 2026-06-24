

from sqlalchemy.orm import sessionmaker, joinedload
from models import engine, Department, Student, Course, Enrollment

Session = sessionmaker(bind=engine)
session = Session()

d1 = Department(dept_name="Computer Science")
d2 = Department(dept_name="Electronics")
d3 = Department(dept_name="Mechanical")

session.add_all([d1, d2, d3])
session.commit()

s1 = Student(
    student_name="Arun",
    email="arun@gmail.com",
    enrollment_year=2022,
    department=d1
)

s2 = Student(
    student_name="Priya",
    email="priya@gmail.com",
    enrollment_year=2023,
    department=d1
)

s3 = Student(
    student_name="Kavin",
    email="kavin@gmail.com",
    enrollment_year=2022,
    department=d2
)

s4 = Student(
    student_name="Meena",
    email="meena@gmail.com",
    enrollment_year=2021,
    department=d3
)

s5 = Student(
    student_name="Rahul",
    email="rahul@gmail.com",
    enrollment_year=2023,
    department=d2
)

session.add_all([s1, s2, s3, s4, s5])
session.commit()

c1 = Course(course_name="Python Programming")
c2 = Course(course_name="Database Systems")
c3 = Course(course_name="Java Programming")

session.add_all([c1, c2, c3])
session.commit()

e1 = Enrollment(student=s1, course=c1)
e2 = Enrollment(student=s1, course=c2)
e3 = Enrollment(student=s2, course=c1)
e4 = Enrollment(student=s3, course=c3)

session.add_all([e1, e2, e3, e4])
session.commit()

students = (
    session.query(Student)
    .join(Department)
    .filter(Department.dept_name == "Computer Science")
    .all()
)

print("\nStudents in Computer Science Department:")
for student in students:
    print(student.student_name)

print("\nEnrollment Details (Normal Query):")

enrollments = session.query(Enrollment).all()

for enrollment in enrollments:
    print(
        enrollment.student.student_name,
        "->",
        enrollment.course.course_name
    )

print("\nEnrollment Details (joinedload):")

enrollments = (
    session.query(Enrollment)
    .options(
        joinedload(Enrollment.student),
        joinedload(Enrollment.course)
    )
    .all()
)

for enrollment in enrollments:
    print(
        enrollment.student.student_name,
        "->",
        enrollment.course.course_name
    )

student = (
    session.query(Student)
    .filter(Student.email == "arun@gmail.com")
    .first()
)

if student:
    student.enrollment_year = 2024
    session.commit()

enrollment = session.query(Enrollment).first()

if enrollment:
    session.delete(enrollment)
    session.commit()

session.close()