# main.py — Hands-On 7: Complete CRUD + Background Tasks + OpenAPI customisation.
# Builds on Hands-On 6 by adding Students, Enrollments, background tasks,
# and richer OpenAPI documentation.

from fastapi import FastAPI, Depends, HTTPException, BackgroundTasks, status
from sqlalchemy.orm import Session
from typing import List

import models, schemas
from database import engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title='Course Management API',
    description="""
## Course Management API

Manage departments, courses, students, and enrollments for a college system.

### Features
- Full CRUD for all resources
- Async-ready endpoints
- Background task support for email notifications
    """,
    version='1.0.0',
    contact={'name': 'Backend Team', 'email': 'api@college.edu'},
)


# ── Background task helper ────────────────────────────────────────
def send_confirmation_email(student_email: str, course_name: str):
    """
    Simulates sending an enrollment confirmation email.
    Runs AFTER the response is already sent to the client — the client
    doesn't wait for this. Useful for non-critical async work like
    notifications, logging, or cache warming.
    """
    print(f'[EMAIL] Sending enrollment confirmation to {student_email} for {course_name}')


# ── Courses (same as HO6, shown for completeness) ────────────────
@app.get('/api/courses/', response_model=List[schemas.CourseResponse], tags=['Courses'])
def list_courses(db: Session = Depends(get_db)):
    return db.query(models.Course).all()


@app.post('/api/courses/', response_model=schemas.CourseResponse,
          status_code=status.HTTP_201_CREATED, tags=['Courses'])
def create_course(course: schemas.CourseCreate, db: Session = Depends(get_db)):
    db_course = models.Course(**course.model_dump())
    db.add(db_course)
    db.commit()
    db.refresh(db_course)
    return db_course


@app.get('/api/courses/{course_id}', response_model=schemas.CourseResponse, tags=['Courses'])
def get_course(course_id: int, db: Session = Depends(get_db)):
    course = db.query(models.Course).filter(models.Course.id == course_id).first()
    if not course:
        raise HTTPException(404, detail=f'Course {course_id} not found')
    return course


@app.put('/api/courses/{course_id}', response_model=schemas.CourseResponse, tags=['Courses'])
def update_course(course_id: int, data: schemas.CourseCreate, db: Session = Depends(get_db)):
    course = db.query(models.Course).filter(models.Course.id == course_id).first()
    if not course:
        raise HTTPException(404, detail=f'Course {course_id} not found')
    for k, v in data.model_dump().items():
        setattr(course, k, v)
    db.commit(); db.refresh(course)
    return course


@app.delete('/api/courses/{course_id}', status_code=status.HTTP_204_NO_CONTENT, tags=['Courses'])
def delete_course(course_id: int, db: Session = Depends(get_db)):
    course = db.query(models.Course).filter(models.Course.id == course_id).first()
    if not course:
        raise HTTPException(404, detail=f'Course {course_id} not found')
    db.delete(course); db.commit()


@app.get('/api/courses/{course_id}/students', response_model=List[schemas.StudentResponse], tags=['Courses'])
def course_students(course_id: int, db: Session = Depends(get_db)):
    """Returns all students enrolled in the given course via a JOIN"""
    course = db.query(models.Course).filter(models.Course.id == course_id).first()
    if not course:
        raise HTTPException(404, detail='Course not found')
    students = (
        db.query(models.Student)
        .join(models.Enrollment, models.Enrollment.student_id == models.Student.id)
        .filter(models.Enrollment.course_id == course_id)
        .all()
    )
    return students


# ── Students ──────────────────────────────────────────────────────
@app.get('/api/students/', response_model=List[schemas.StudentResponse], tags=['Students'])
def list_students(db: Session = Depends(get_db)):
    return db.query(models.Student).all()


@app.post('/api/students/', response_model=schemas.StudentResponse,
          status_code=status.HTTP_201_CREATED, tags=['Students'])
def create_student(student: schemas.StudentCreate, db: Session = Depends(get_db)):
    db_student = models.Student(**student.model_dump())
    db.add(db_student); db.commit(); db.refresh(db_student)
    return db_student


# ── Enrollments (with background task) ────────────────────────────
class EnrollmentCreate(schemas.BaseModel if False else object):
    pass

from pydantic import BaseModel

class EnrollmentCreate(BaseModel):
    student_id: int
    course_id:  int


@app.post('/api/enrollments/', status_code=status.HTTP_201_CREATED, tags=['Enrollments'])
def create_enrollment(
    data:             EnrollmentCreate,
    background_tasks: BackgroundTasks,
    db:               Session = Depends(get_db)
):
    """
    Enrolls a student in a course.
    After saving to the database, a background task fires to send a
    confirmation email — the response returns immediately without waiting.
    """
    student = db.query(models.Student).filter(models.Student.id == data.student_id).first()
    course  = db.query(models.Course).filter(models.Course.id  == data.course_id).first()

    if not student:
        raise HTTPException(404, detail='Student not found')
    if not course:
        raise HTTPException(404, detail='Course not found')

    enrollment = models.Enrollment(student_id=data.student_id, course_id=data.course_id)
    db.add(enrollment); db.commit(); db.refresh(enrollment)

    # This runs AFTER the 201 response is sent — client doesn't wait
    background_tasks.add_task(send_confirmation_email, student.email, course.name)

    return {'id': enrollment.id, 'student_id': data.student_id, 'course_id': data.course_id}
