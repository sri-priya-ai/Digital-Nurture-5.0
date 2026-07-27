"""
schemas.py
Pydantic models used to validate request bodies and shape response data.
Keeping these separate from the SQLAlchemy models means the API never
leaks internal database fields by accident.
"""

from datetime import date
from typing import Optional
from pydantic import BaseModel, EmailStr, Field, ConfigDict


# ---------- Department ----------
class DepartmentBase(BaseModel):
    name: str
    head_of_dept: Optional[str] = None
    budget: float = 0.0


class DepartmentCreate(DepartmentBase):
    pass


class DepartmentResponse(DepartmentBase):
    id: int
    model_config = ConfigDict(from_attributes=True)


# ---------- Course ----------
class CourseCreate(BaseModel):
    name: str
    code: str
    credits: int = Field(gt=0, le=10)
    department_id: int


class CourseUpdate(BaseModel):
    """All fields optional -> used for PUT/PATCH."""
    name: Optional[str] = None
    code: Optional[str] = None
    credits: Optional[int] = Field(default=None, gt=0, le=10)
    department_id: Optional[int] = None


class CourseResponse(BaseModel):
    id: int
    name: str
    code: str
    credits: int
    department_id: int
    model_config = ConfigDict(from_attributes=True)


# ---------- Student ----------
class StudentCreate(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    department_id: Optional[int] = None
    enrollment_year: Optional[int] = None


class StudentUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[EmailStr] = None
    department_id: Optional[int] = None
    enrollment_year: Optional[int] = None


class StudentResponse(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: EmailStr
    department_id: Optional[int] = None
    enrollment_year: Optional[int] = None
    model_config = ConfigDict(from_attributes=True)


# ---------- Enrollment ----------
class EnrollmentCreate(BaseModel):
    student_id: int
    course_id: int
    enrollment_date: Optional[date] = None
    grade: Optional[str] = None


class EnrollmentResponse(BaseModel):
    id: int
    student_id: int
    course_id: int
    enrollment_date: Optional[date] = None
    grade: Optional[str] = None
    model_config = ConfigDict(from_attributes=True)


# ---------- Pagination envelope (DRF-style) ----------
class PaginatedCourseResponse(BaseModel):
    count: int
    next: Optional[str] = None
    previous: Optional[str] = None
    results: list[CourseResponse]


# ---------- Auth ----------
class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8)


class UserResponse(BaseModel):
    id: int
    email: EmailStr
    is_active: bool
    model_config = ConfigDict(from_attributes=True)


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    email: Optional[str] = None


