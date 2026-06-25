# models.py — SQLAlchemy ORM models (database table definitions).
# Separate from Pydantic schemas — these map to actual DB tables.

from sqlalchemy import Column, Integer, String, ForeignKey, Numeric, UniqueConstraint
from sqlalchemy.orm import relationship
from database import Base


class Department(Base):
    __tablename__ = 'department'
    id           = Column(Integer, primary_key=True, index=True)
    name         = Column(String(120), nullable=False)
    head_of_dept = Column(String(120))
    budget       = Column(Numeric(12, 2), default=0)
    courses      = relationship('Course', back_populates='department')


class Course(Base):
    __tablename__ = 'course'
    id            = Column(Integer, primary_key=True, index=True)
    name          = Column(String(200), nullable=False)
    code          = Column(String(20),  unique=True, nullable=False)
    credits       = Column(Integer, nullable=False)
    department_id = Column(Integer, ForeignKey('department.id'), nullable=False)
    department    = relationship('Department', back_populates='courses')
    enrollments   = relationship('Enrollment', back_populates='course')


class Student(Base):
    __tablename__ = 'student'
    id              = Column(Integer, primary_key=True, index=True)
    first_name      = Column(String(80),  nullable=False)
    last_name       = Column(String(80),  nullable=False)
    email           = Column(String(200), unique=True, nullable=False)
    department_id   = Column(Integer, ForeignKey('department.id'), nullable=True)
    enrollment_year = Column(Integer)
    enrollments     = relationship('Enrollment', back_populates='student')


class Enrollment(Base):
    __tablename__  = 'enrollment'
    __table_args__ = (UniqueConstraint('student_id', 'course_id'),)
    id         = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey('student.id'),  nullable=False)
    course_id  = Column(Integer, ForeignKey('course.id'),   nullable=False)
    grade      = Column(String(5), nullable=True)
    student    = relationship('Student', back_populates='enrollments')
    course     = relationship('Course',  back_populates='enrollments')
