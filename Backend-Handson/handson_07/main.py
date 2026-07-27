"""
main.py - Hands-On 7
FastAPI - Dependency Injection, CRUD & OpenAPI Documentation

Run with:
    uvicorn main:app --reload
Then visit http://127.0.0.1:8000/docs
"""

from fastapi import FastAPI, Depends, HTTPException, status, BackgroundTasks
from sqlalchemy.orm import Session
from sqlalchemy import select

import models
import schemas
from database import engine, get_db

# Create all tables on startup (fine for a hands-on exercise; in a real
# project you would use Alembic migrations instead).
models.Base.metadata.create_all(bind=engine)

# ---------------------------------------------------------------------------
# Step 75: Customise OpenAPI metadata (title, description, version, contact)
# ---------------------------------------------------------------------------
app = FastAPI(
    title="Course Management API",
    description=(
        "API for managing departments, courses, students and enrollments "
        "for the Digital Nurture 5.0 Course Management System."
    ),
    version="1.0.0",
    contact={
        "name": "API Support",
        "email": "support@coursemanager.example.com",
    },
)


def send_confirmation_email(student_email: str):
    """
    Step 73: Simulates sending a confirmation email.
    This runs in the background AFTER the response has already
    been sent back to the client.
    """
    print(f"Sending confirmation to {student_email}")


# ---------------------------------------------------------------------------
# Root
# ---------------------------------------------------------------------------
@app.get("/", tags=["Root"])
def read_root():
    return {"message": "Course Management API is running"}


# ---------------------------------------------------------------------------
# Departments (minimal CRUD - courses/students reference these by id)
# ---------------------------------------------------------------------------
@app.get("/api/departments/", response_model=list[schemas.DepartmentResponse], tags=["Departments"])
def list_departments(db: Session = Depends(get_db)):
    return db.query(models.Department).all()


@app.post(
    "/api/departments/",
    response_model=schemas.DepartmentResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["Departments"],
)
def create_department(department: schemas.DepartmentCreate, db: Session = Depends(get_db)):
    db_department = models.Department(**department.model_dump())
    db.add(db_department)
    db.commit()
    db.refresh(db_department)
    return db_department


@app.get("/api/departments/{department_id}", response_model=schemas.DepartmentResponse, tags=["Departments"])
def get_department(department_id: int, db: Session = Depends(get_db)):
    department = db.get(models.Department, department_id)
    if department is None:
        raise HTTPException(status_code=404, detail="Department not found")
    return department


# ---------------------------------------------------------------------------
# Courses  (Step 68-70: full CRUD with correct status codes / response models)
# ---------------------------------------------------------------------------
@app.get("/api/courses/", response_model=list[schemas.CourseResponse], tags=["Courses"])
def list_courses(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    courses = db.execute(select(models.Course).offset(skip).limit(limit)).scalars().all()
    return courses


@app.post(
    "/api/courses/",
    response_model=schemas.CourseResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["Courses"],
    summary="Create a new course",
    response_description="The newly created course",
)
def create_course(course: schemas.CourseCreate, db: Session = Depends(get_db)):
    db_course = models.Course(**course.model_dump())
    db.add(db_course)
    db.commit()
    db.refresh(db_course)
    return db_course


@app.get("/api/courses/{course_id}", response_model=schemas.CourseResponse, tags=["Courses"])
def get_course(course_id: int, db: Session = Depends(get_db)):
    course = db.get(models.Course, course_id)
    if course is None:
        raise HTTPException(status_code=404, detail="Course not found")
    return course


@app.put("/api/courses/{course_id}", response_model=schemas.CourseResponse, tags=["Courses"])
def update_course(course_id: int, payload: schemas.CourseUpdate, db: Session = Depends(get_db)):
    course = db.get(models.Course, course_id)
    if course is None:
        raise HTTPException(status_code=404, detail="Course not found")

    update_data = payload.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(course, field, value)

    db.commit()
    db.refresh(course)
    return course


@app.delete("/api/courses/{course_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Courses"])
def delete_course(course_id: int, db: Session = Depends(get_db)):
    course = db.get(models.Course, course_id)
    if course is None:
        raise HTTPException(status_code=404, detail="Course not found")
    db.delete(course)
    db.commit()
    # 204 No Content -> no response body is returned
    return None


@app.get(
    "/api/courses/{course_id}/students/",
    response_model=list[schemas.StudentResponse],
    tags=["Courses"],
)
def get_students_for_course(course_id: int, db: Session = Depends(get_db)):
    """Step 71: JOIN query - all students enrolled in a given course."""
    course = db.get(models.Course, course_id)
    if course is None:
        raise HTTPException(status_code=404, detail="Course not found")

    students = (
        db.query(models.Student)
        .join(models.Enrollment, models.Enrollment.student_id == models.Student.id)
        .filter(models.Enrollment.course_id == course_id)
        .all()
    )
    return students


# ---------------------------------------------------------------------------
# Students (Step 72: same CRUD pattern as courses)
# ---------------------------------------------------------------------------
@app.get("/api/students/", response_model=list[schemas.StudentResponse], tags=["Students"])
def list_students(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    students = db.execute(select(models.Student).offset(skip).limit(limit)).scalars().all()
    return students


@app.post(
    "/api/students/",
    response_model=schemas.StudentResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["Students"],
)
def create_student(student: schemas.StudentCreate, db: Session = Depends(get_db)):
    existing = db.query(models.Student).filter(models.Student.email == student.email).first()
    if existing:
        raise HTTPException(status_code=409, detail="Email already registered")

    db_student = models.Student(**student.model_dump())
    db.add(db_student)
    db.commit()
    db.refresh(db_student)
    return db_student


@app.get("/api/students/{student_id}", response_model=schemas.StudentResponse, tags=["Students"])
def get_student(student_id: int, db: Session = Depends(get_db)):
    student = db.get(models.Student, student_id)
    if student is None:
        raise HTTPException(status_code=404, detail="Student not found")
    return student


@app.put("/api/students/{student_id}", response_model=schemas.StudentResponse, tags=["Students"])
def update_student(student_id: int, payload: schemas.StudentUpdate, db: Session = Depends(get_db)):
    student = db.get(models.Student, student_id)
    if student is None:
        raise HTTPException(status_code=404, detail="Student not found")

    update_data = payload.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(student, field, value)

    db.commit()
    db.refresh(student)
    return student


@app.delete("/api/students/{student_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Students"])
def delete_student(student_id: int, db: Session = Depends(get_db)):
    student = db.get(models.Student, student_id)
    if student is None:
        raise HTTPException(status_code=404, detail="Student not found")
    db.delete(student)
    db.commit()
    return None


# ---------------------------------------------------------------------------
# Enrollments (Step 73-74: Background Tasks)
# ---------------------------------------------------------------------------
@app.post(
    "/api/enrollments/",
    response_model=schemas.EnrollmentResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["Enrollments"],
)
def create_enrollment(
    enrollment: schemas.EnrollmentCreate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
):
    student = db.get(models.Student, enrollment.student_id)
    if student is None:
        raise HTTPException(status_code=404, detail="Student not found")

    course = db.get(models.Course, enrollment.course_id)
    if course is None:
        raise HTTPException(status_code=404, detail="Course not found")

    already_enrolled = (
        db.query(models.Enrollment)
        .filter_by(student_id=enrollment.student_id, course_id=enrollment.course_id)
        .first()
    )
    if already_enrolled:
        raise HTTPException(status_code=409, detail="Student already enrolled in this course")

    db_enrollment = models.Enrollment(**enrollment.model_dump())
    db.add(db_enrollment)
    db.commit()
    db.refresh(db_enrollment)

    # Response is returned immediately; this task runs afterwards.
    background_tasks.add_task(send_confirmation_email, student.email)

    return db_enrollment


@app.get("/api/enrollments/", response_model=list[schemas.EnrollmentResponse], tags=["Enrollments"])
def list_enrollments(db: Session = Depends(get_db)):
    return db.query(models.Enrollment).all()


@app.delete("/api/enrollments/{enrollment_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Enrollments"])
def delete_enrollment(enrollment_id: int, db: Session = Depends(get_db)):
    enrollment = db.get(models.Enrollment, enrollment_id)
    if enrollment is None:
        raise HTTPException(status_code=404, detail="Enrollment not found")
    db.delete(enrollment)
    db.commit()
    return None
