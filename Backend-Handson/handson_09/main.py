"""
main.py - Hands-On 9
Authentication & Security - JWT, OAuth2 & OWASP

Builds on Hands-On 8's API and adds:
  - bcrypt password hashing + user registration
  - JWT login
  - route protection via a get_current_user dependency
  - CORS configuration for a frontend dev server

Run with:
    uvicorn main:app --reload
Then visit http://127.0.0.1:8000/docs

--------------------------------------------------------------------------
Step 95 note - OAuth2 Authorization Code flow vs. this simple JWT login:

The OAuth2 Authorization Code flow is designed for THIRD-PARTY delegated
access (e.g. "Sign in with Google", or a third-party app that wants
limited access to a user's account on another service). It involves:
  1. The client redirects the user to the Authorization Server's login
     page (e.g. Google's login page) - the client never sees the
     user's password.
  2. The user logs in and approves the requested scopes.
  3. The Authorization Server redirects back to the client with a
     short-lived "authorization code".
  4. The client exchanges that code (plus a client secret, server-side)
     for an access token and refresh token.

The JWT login implemented here is much simpler: the client (our own
frontend) sends the user's email/password DIRECTLY to our own API,
which verifies them and hands back a JWT. This is appropriate because
we ARE the resource owner AND the authorization server - there is no
third party involved and no need for a redirect/consent step. This
pattern is sometimes called the OAuth2 "Password" grant (or, outside
OAuth2 entirely, just "JWT-based authentication").
--------------------------------------------------------------------------
"""

from fastapi import FastAPI, Depends, HTTPException, Request, Response, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from sqlalchemy import select, or_

import models
import schemas
import security
from database import engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Course Management API",
    description="Course Management API with JWT authentication.",
    version="3.0.0",
)

# ---------------------------------------------------------------------------
# Step 94: CORS - allow the frontend dev server to call this API
# ---------------------------------------------------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------------------------------------------------------
# Standardised error response format (carried over from Hands-On 8)
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
    code = ERROR_CODE_BY_STATUS.get(exc.status_code, "ERROR")
    headers = getattr(exc, "headers", None)
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": {"code": code, "message": exc.detail, "field": None}},
        headers=headers,
    )


def not_found(resource: str):
    raise HTTPException(status_code=404, detail=f"{resource} not found")


# ---------------------------------------------------------------------------
# Auth: registration, login, and the get_current_user dependency
# ---------------------------------------------------------------------------
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login/")


@app.post(
    "/api/v1/auth/register/",
    response_model=schemas.UserResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["Auth"],
)
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    """Step 88: register a new user. Password is hashed, never stored/logged in plain text."""
    existing = db.query(models.User).filter(models.User.email == user.email).first()
    if existing:
        raise HTTPException(status_code=409, detail="Email already registered")

    db_user = models.User(
        email=user.email,
        hashed_password=security.get_password_hash(user.password),
        is_active=True,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


@app.post("/api/v1/auth/login/", response_model=schemas.Token, tags=["Auth"])
def login(credentials: schemas.UserLogin, db: Session = Depends(get_db)):
    """Step 91: verify credentials and return a JWT access token."""
    user = db.query(models.User).filter(models.User.email == credentials.email).first()
    if not user or not security.verify_password(credentials.password, user.hashed_password):
        raise HTTPException(
            status_code=401,
            detail="Incorrect email or password",
        )

    access_token = security.create_access_token(data={"sub": user.email})
    return schemas.Token(access_token=access_token, token_type="bearer")


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> models.User:
    """Step 92: decode and validate the JWT, returning the current user."""
    credentials_error = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    payload = security.decode_access_token(token)
    if payload is None:
        raise credentials_error

    email = payload.get("sub")
    if email is None:
        raise credentials_error

    user = db.query(models.User).filter(models.User.email == email).first()
    if user is None:
        raise credentials_error
    return user


@app.get("/api/v1/auth/me/", response_model=schemas.UserResponse, tags=["Auth"])
def read_current_user(current_user: models.User = Depends(get_current_user)):
    return current_user


# ---------------------------------------------------------------------------
# Departments
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
    response.headers["Location"] = f"/api/v1/departments/{db_department.id}"
    return db_department


# ---------------------------------------------------------------------------
# Courses - GET/list are public; create/delete require a valid JWT (Step 93)
# ---------------------------------------------------------------------------
@app.get("/api/v1/courses/", response_model=schemas.PaginatedCourseResponse, tags=["Courses"])
def list_courses(
    request: Request,
    page: int = 1,
    page_size: int = 10,
    search: str | None = None,
    db: Session = Depends(get_db),
):
    if page < 1:
        raise HTTPException(status_code=400, detail="page must be >= 1")
    if page_size < 1 or page_size > 100:
        raise HTTPException(status_code=400, detail="page_size must be between 1 and 100")

    query = db.query(models.Course)
    if search:
        like_pattern = f"%{search}%"
        query = query.filter(
            or_(models.Course.name.ilike(like_pattern), models.Course.code.ilike(like_pattern))
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

    return schemas.PaginatedCourseResponse(
        count=total_count,
        next=build_url(page + 1) if offset + page_size < total_count else None,
        previous=build_url(page - 1) if page > 1 else None,
        results=results,
    )


@app.post(
    "/api/v1/courses/",
    response_model=schemas.CourseResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["Courses"],
)
def create_course(
    course: schemas.CourseCreate,
    response: Response,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),  # Step 93: protected
):
    db_course = models.Course(**course.model_dump())
    db.add(db_course)
    db.commit()
    db.refresh(db_course)
    response.headers["Location"] = f"/api/v1/courses/{db_course.id}"
    return db_course


@app.get("/api/v1/courses/{course_id}", response_model=schemas.CourseResponse, tags=["Courses"])
def get_course(course_id: int, db: Session = Depends(get_db)):
    course = db.get(models.Course, course_id)
    if course is None:
        not_found("Course")
    return course


@app.patch("/api/v1/courses/{course_id}", response_model=schemas.CourseResponse, tags=["Courses"])
def partial_update_course(
    course_id: int,
    payload: schemas.CourseUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    course = db.get(models.Course, course_id)
    if course is None:
        not_found("Course")
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(course, field, value)
    db.commit()
    db.refresh(course)
    return course


@app.delete("/api/v1/courses/{course_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Courses"])
def delete_course(
    course_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),  # Step 93: protected
):
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
