# main.py — FastAPI application entry point.
# Run with: uvicorn main:app --reload
# Swagger UI auto-generated at: http://127.0.0.1:8000/docs

from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional

import models, schemas
from database import engine, get_db

# Creates all tables on startup if they don't already exist
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title='Course Management API',
    description='A REST API for managing college courses, students and enrollments.',
    version='1.0.0',
    contact={'name': 'Backend Team', 'email': 'api@college.edu'},
)


@app.get('/')
def root():
    return {'message': 'Course Management API is running', 'docs': '/docs'}


# ── Courses ──────────────────────────────────────────────────────

@app.get('/api/courses/', response_model=List[schemas.CourseResponse], tags=['Courses'])
def list_courses(
    skip:          int           = 0,
    limit:         int           = 10,
    department_id: Optional[int] = None,
    db:            Session       = Depends(get_db)
):
    """
    List all courses with optional pagination and department filter.
    - skip / limit implement offset pagination
    - department_id filters to a single department's courses
    """
    query = db.query(models.Course)
    if department_id:
        query = query.filter(models.Course.department_id == department_id)
    return query.offset(skip).limit(limit).all()


@app.post('/api/courses/', response_model=schemas.CourseResponse,
          status_code=status.HTTP_201_CREATED, tags=['Courses'],
          summary='Create a new course',
          response_description='The newly created course')
def create_course(course: schemas.CourseCreate, db: Session = Depends(get_db)):
    """
    Creates a new course. FastAPI validates the request body against
    CourseCreate automatically — invalid data returns 422 before this runs.
    """
    db_course = models.Course(**course.model_dump())
    db.add(db_course)
    db.commit()
    db.refresh(db_course)
    return db_course


@app.get('/api/courses/{course_id}', response_model=schemas.CourseResponse, tags=['Courses'])
def get_course(course_id: int, db: Session = Depends(get_db)):
    course = db.query(models.Course).filter(models.Course.id == course_id).first()
    if not course:
        # FastAPI converts HTTPException to a JSON error response automatically
        raise HTTPException(status_code=404, detail=f'Course {course_id} not found')
    return course


@app.put('/api/courses/{course_id}', response_model=schemas.CourseResponse, tags=['Courses'])
def update_course(course_id: int, updated: schemas.CourseCreate, db: Session = Depends(get_db)):
    course = db.query(models.Course).filter(models.Course.id == course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail=f'Course {course_id} not found')
    for field, value in updated.model_dump().items():
        setattr(course, field, value)
    db.commit()
    db.refresh(course)
    return course


@app.delete('/api/courses/{course_id}', status_code=status.HTTP_204_NO_CONTENT, tags=['Courses'])
def delete_course(course_id: int, db: Session = Depends(get_db)):
    course = db.query(models.Course).filter(models.Course.id == course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail=f'Course {course_id} not found')
    db.delete(course)
    db.commit()
    # 204 means no body in the response
