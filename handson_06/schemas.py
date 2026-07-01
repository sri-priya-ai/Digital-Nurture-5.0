from pydantic import BaseModel
from typing import Optional, List


class CourseIn(BaseModel):
    course_title: str
    course_code: str
    credit_hrs: int
    dept_id: int


class CourseEdit(BaseModel):
    course_title: Optional[str] = None
    course_code: Optional[str] = None
    credit_hrs: Optional[int] = None
    dept_id: Optional[int] = None


class CourseOut(BaseModel):
    course_id: int
    course_title: str
    course_code: str
    credit_hrs: int
    dept_id: int

    class Config:
        from_attributes = True


class DeptOut(BaseModel):
    dept_id: int
    dept_name: str
    dept_head: Optional[str] = None
    courses: List[CourseOut] = []

    class Config:
        from_attributes = True
