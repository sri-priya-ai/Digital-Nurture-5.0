"""
main.py - Hands-On 8
RESTful API Design Best Practices

Builds on Hands-On 7's Course Management API and refactors it to follow
REST conventions: versioned URLs, PATCH support, Location headers,
DRF-style pagination envelopes, search filtering, and a standardised
error response format.

Run with:
    uvicorn main:app --reload
Then visit http://127.0.0.1:8000/docs

--------------------------------------------------------------------------
Step 82 note - API versioning strategies:
  1. URL versioning (used here, e.g. /api/v1/courses/):
     - Simple, visible, easy to test directly in a browser.
     - Downside: the URL changes between versions, so old links/bookmarks
       to a resource change meaning across versions.
  2. Header-based versioning (e.g. Accept: application/vnd.api+json;version=1):
     - Keeps URLs clean/stable across versions (same URL, different
       representation negotiated via headers).
     - Downside: harder to test manually (can't just paste a URL in a
       browser), and less discoverable/explicit for API consumers.
--------------------------------------------------------------------------
"""

from fastapi import FastAPI, Depends, HTTPException, Request, Response, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from sqlalchemy import select, or_, func

import models
import schemas
from database import engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Course Management API",
    description="REST-best-practices refactor of the Course Management API.",
    version="2.0.0",
)


# ---------------------------------------------------------------------------
# Step 85: Standardised error response format
#   {'error': {'code': 'NOT_FOUND', 'message': '...', 'field': null}}
# ---------------------------------------------------------------------------
ERROR_CODE_BY_STATUS = {
    400: "BAD_REQUEST",
    401: "UNAUTHORIZED",
    404: "NOT_FOUND",
    409: "CONFLICT",
    422: "UNPROCESSABLE_ENTITY",
}


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    """Converts every HTTPException into the standardised error envelope."""
    code = ERROR_CODE_BY_STATUS.get(exc.status_code, "ERROR")
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": {
                "code": code,
                "message": exc.detail,
                "field": None,
            }
        },
    )


def not_found(resource: str):
    raise HTTPException(status_code=404, detail=f"{resource} not found")


# ---------------------------------------------------------------------------
# Departments (minimal CRUD - referenced by courses/students)
# ---------------------------------------------------------------------------
@app.get("/api/v1/departments/", response_model=list[schemas.DepartmentResponse], tags=["Departments"])
def list_departments(db: Session = Depends(get_db)):
    return db.query(models.Department).all()


@app.post(
    "/api/v1/departments/",
    response_model=schemas.DepartmentResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["Departments"],
)
def create_department(department: schemas.DepartmentCreate, response: Response, db: Session = Depends(get_db)):
    db_department = models.Department(**department.model_dump())
    db.add(db_department)
    db.commit()
    db.refresh(db_department)
    # Step 81: Location header pointing to the new resource
    response.headers["Location"] = f"/api/v1/departments/{db_department.id}"
    return db_department


@app.get("/api/v1/departments/{department_id}", response_model=schemas.DepartmentResponse, tags=["Departments"])
def get_department(department_id: int, db: Session = Depends(get_db)):
    department = db.get(models.Department, department_id)
    if department is None:
        not_found("Department")
    return department


# ---------------------------------------------------------------------------
# Courses - versioned, paginated, filterable, PATCH-able
# ---------------------------------------------------------------------------
@app.get("/api/v1/courses/", response_model=schemas.PaginatedCourseResponse, tags=["Courses"])
def list_courses(
    request: Request,
    page: int = 1,
    page_size: int = 10,
    search: str | None = None,
    db: Session = Depends(get_db),
):
    """
    Step 83: Offset pagination with a DRF-style envelope.
    Step 84: Case-insensitive search across course name and code.
    """
    if page < 1:
        raise HTTPException(status_code=400, detail="page must be >= 1")
    if page_size < 1 or page_size > 100:
        raise HTTPException(status_code=400, detail="page_size must be between 1 and 100")

    query = db.query(models.Course)
    if search:
        like_pattern = f"%{search}%"
        query = query.filter(
            or_(
                models.Course.name.ilike(like_pattern),
                models.Course.code.ilike(like_pattern),
            )
        )

    total_count = query.count()
    offset = (page - 1) * page_size
    results = query.offset(offset).limit(page_size).all()

    base_url = str(request.url).split("?")[0]

    def build_url(target_page: int) -> str | None:
        if target_page < 1:
            return None
        max_page = max((total_count - 1) // page_size + 1, 1)
        if target_page > max_page:
            return None
        qs = f"page={target_page}&page_size={page_size}"
        if search:
            qs += f"&search={search}"
        return f"{base_url}?{qs}"

    next_url = build_url(page + 1) if offset + page_size < total_count else None
    previous_url = build_url(page - 1) if page > 1 else None

    return schemas.PaginatedCourseResponse(
        count=total_count,
        next=next_url,
        previous=previous_url,
        results=results,
    )


@app.post(
    "/api/v1/courses/",
    response_model=schemas.CourseResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["Courses"],
)
def create_course(course: schemas.CourseCreate, response: Response, db: Session = Depends(get_db)):
    db_course = models.Course(**course.model_dump())
    db.add(db_course)
    db.commit()
    db.refresh(db_course)
    # Step 81: Location header on POST
    response.headers["Location"] = f"/api/v1/courses/{db_course.id}"
    return db_course


@app.get("/api/v1/courses/{course_id}", response_model=schemas.CourseResponse, tags=["Courses"])
def get_course(course_id: int, db: Session = Depends(get_db)):
    course = db.get(models.Course, course_id)
    if course is None:
        not_found("Course")
    return course


@app.put("/api/v1/courses/{course_id}", response_model=schemas.CourseResponse, tags=["Courses"])
def replace_course(course_id: int, payload: schemas.CourseCreate, db: Session = Depends(get_db)):
    """PUT = full replace, every field required."""
    course = db.get(models.Course, course_id)
    if course is None:
        not_found("Course")
    for field, value in payload.model_dump().items():
        setattr(course, field, value)
    db.commit()
    db.refresh(course)
    return course


@app.patch("/api/v1/courses/{course_id}", response_model=schemas.CourseResponse, tags=["Courses"])
def partial_update_course(course_id: int, payload: schemas.CourseUpdate, db: Session = Depends(get_db)):
    """Step 79: PATCH = partial update, only supplied fields are changed."""
    course = db.get(models.Course, course_id)
    if course is None:
        not_found("Course")
    update_data = payload.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(course, field, value)
    db.commit()
    db.refresh(course)
    return course


@app.delete("/api/v1/courses/{course_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Courses"])
def delete_course(course_id: int, db: Session = Depends(get_db)):
    course = db.get(models.Course, course_id)
    if course is None:
        not_found("Course")
    db.delete(course)
    db.commit()
    return None


# ---------------------------------------------------------------------------
# Students
# ---------------------------------------------------------------------------
@app.get("/api/v1/students/", response_model=list[schemas.StudentResponse], tags=["Students"])
def list_students(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return db.execute(select(models.Student).offset(skip).limit(limit)).scalars().all()


@app.post(
    "/api/v1/students/",
    response_model=schemas.StudentResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["Students"],
)
def create_student(student: schemas.StudentCreate, response: Response, db: Session = Depends(get_db)):
    existing = db.query(models.Student).filter(models.Student.email == student.email).first()
    if existing:
        raise HTTPException(status_code=409, detail="Email already registered")
    db_student = models.Student(**student.model_dump())
    db.add(db_student)
    db.commit()
    db.refresh(db_student)
    response.headers["Location"] = f"/api/v1/students/{db_student.id}"
    return db_student


@app.get("/api/v1/students/{student_id}", response_model=schemas.StudentResponse, tags=["Students"])
def get_student(student_id: int, db: Session = Depends(get_db)):
    student = db.get(models.Student, student_id)
    if student is None:
        not_found("Student")
    return student


@app.patch("/api/v1/students/{student_id}", response_model=schemas.StudentResponse, tags=["Students"])
def partial_update_student(student_id: int, payload: schemas.StudentUpdate, db: Session = Depends(get_db)):
    student = db.get(models.Student, student_id)
    if student is None:
        not_found("Student")
    update_data = payload.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(student, field, value)
    db.commit()
    db.refresh(student)
    return student


@app.delete("/api/v1/students/{student_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Students"])
def delete_student(student_id: int, db: Session = Depends(get_db)):
    student = db.get(models.Student, student_id)
    if student is None:
        not_found("Student")
    db.delete(student)
    db.commit()
    return None


# ---------------------------------------------------------------------------
# Enrollments
# ---------------------------------------------------------------------------
@app.post(
    "/api/v1/enrollments/",
    response_model=schemas.EnrollmentResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["Enrollments"],
)
def create_enrollment(enrollment: schemas.EnrollmentCreate, response: Response, db: Session = Depends(get_db)):
    if db.get(models.Student, enrollment.student_id) is None:
        not_found("Student")
    if db.get(models.Course, enrollment.course_id) is None:
        not_found("Course")

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
    response.headers["Location"] = f"/api/v1/enrollments/{db_enrollment.id}"
    return db_enrollment


@app.get("/api/v1/enrollments/", response_model=list[schemas.EnrollmentResponse], tags=["Enrollments"])
def list_enrollments(db: Session = Depends(get_db)):
    return db.query(models.Enrollment).all()
