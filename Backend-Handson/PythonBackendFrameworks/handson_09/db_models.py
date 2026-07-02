from sqlalchemy import Column, Integer, String, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from database import Base


class Department(Base):
    __tablename__ = 'departments'

    dept_id = Column(Integer, primary_key=True, index=True)
    dept_name = Column(String(150), nullable=False)
    dept_head = Column(String(100))
    courses = relationship('Course', back_populates='dept')


class Course(Base):
    __tablename__ = 'courses'

    course_id = Column(Integer, primary_key=True, index=True)
    course_title = Column(String(200), nullable=False)
    course_code = Column(String(20), unique=True, nullable=False)
    credit_hrs = Column(Integer, nullable=False)
    dept_id = Column(Integer, ForeignKey('departments.dept_id'), nullable=False)
    dept = relationship('Department', back_populates='courses')
    enrollments = relationship('Enrollment', back_populates='course')


class Student(Base):
    __tablename__ = 'students'

    stu_id = Column(Integer, primary_key=True, index=True)
    fname = Column(String(80), nullable=False)
    lname = Column(String(80), nullable=False)
    email_addr = Column(String(120), unique=True, nullable=False)
    join_year = Column(Integer)
    enrollments = relationship('Enrollment', back_populates='student')


class Enrollment(Base):
    __tablename__ = 'enrollments'
    __table_args__ = (UniqueConstraint('stu_id', 'course_id', name='uq_stu_course'),)

    enroll_id = Column(Integer, primary_key=True, index=True)
    stu_id = Column(Integer, ForeignKey('students.stu_id'), nullable=False)
    course_id = Column(Integer, ForeignKey('courses.course_id'), nullable=False)
    student = relationship('Student', back_populates='enrollments')
    course = relationship('Course', back_populates='enrollments')


class AppUser(Base):
    __tablename__ = 'app_users'

    user_id = Column(Integer, primary_key=True, index=True)
    email_addr = Column(String(120), unique=True, nullable=False)
    pwd_hash = Column(String(200), nullable=False)
    is_active = Column(Integer, default=1)
