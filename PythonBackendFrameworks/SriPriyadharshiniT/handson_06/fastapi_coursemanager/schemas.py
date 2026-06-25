# schemas.py — Pydantic models for request validation and response shaping.
# FastAPI uses these to automatically validate incoming JSON and document
# the API in Swagger UI — no extra code needed.

from pydantic import BaseModel
from typing import Optional, List


class CourseCreate(BaseModel):
    """Fields required when creating a new course"""
    name:          str
    code:          str
    credits:       int
    department_id: int


class CourseUpdate(BaseModel):
    """All fields optional for partial updates"""
    name:          Optional[str]   = None
    code:          Optional[str]   = None
    credits:       Optional[int]   = None
    department_id: Optional[int]   = None


class CourseResponse(BaseModel):
    """Shape of the data returned to the client"""
    id:            int
    name:          str
    code:          str
    credits:       int
    department_id: int

    class Config:
        # Allows Pydantic to read data from ORM objects (not just dicts)
        from_attributes = True


class DepartmentCreate(BaseModel):
    name:         str
    head_of_dept: str
    budget:       float = 0.0


class DepartmentResponse(BaseModel):
    id:           int
    name:         str
    head_of_dept: str
    budget:       float
    # Nested list — Pydantic handles the nesting automatically
    courses:      List[CourseResponse] = []

    class Config:
        from_attributes = True


class StudentCreate(BaseModel):
    first_name:      str
    last_name:       str
    email:           str
    department_id:   Optional[int] = None
    enrollment_year: int


class StudentResponse(BaseModel):
    id:              int
    first_name:      str
    last_name:       str
    email:           str
    department_id:   Optional[int]
    enrollment_year: int

    class Config:
        from_attributes = True
