from fastapi import FastAPI, Depends, HTTPException, status, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Optional, List

from database import get_db, async_eng, Base
from db_models import Course, Student, Enrollment
from schemas import CourseIn, CourseEdit, CourseOut, StudentIn, StudentOut, EnrollIn, EnrollOut

app = FastAPI(
    title='Course Management API',
    description='Manage departments, courses, students and enrollments.',
    version='1.0.0',
    contact={'name': 'Admin', 'email': 'admin@college.edu'},
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=['http://localhost:3000'],
    allow_methods=['*'],
    allow_headers=['*'],
)


@app.on_event('startup')
async def init_tables():
    async with async_eng.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


@app.get('/')
async def root():
    return {'message': 'API running'}


@app.get('/api/courses/', response_model=List[CourseOut], tags=['Courses'])
async def list_courses(
    skip: int = 0,
    limit: int = 10,
    dept_id: Optional[int] = None,
    db: AsyncSession = Depends(get_db)
):
    qry = select(Course)
    if dept_id:
        qry = qry.where(Course.dept_id == dept_id)
    res = await db.execute(qry.offset(skip).limit(limit))
    return res.scalars().all()


@app.post(
    '/api/courses/',
    response_model=CourseOut,
    status_code=status.HTTP_201_CREATED,
    tags=['Courses'],
    summary='Create a new course',
    response_description='The newly created course record',
)
async def create_course(payload: CourseIn, db: AsyncSession = Depends(get_db)):
    obj = Course(**payload.dict())
    db.add(obj)
    await db.commit()
    await db.refresh(obj)
    return obj


@app.get('/api/courses/{cid}', response_model=CourseOut, tags=['Courses'])
async def get_course(cid: int, db: AsyncSession = Depends(get_db)):
    res = await db.execute(select(Course).where(Course.course_id == cid))
    obj = res.scalar_one_or_none()
    if not obj:
        raise HTTPException(status_code=404, detail='Course not found')
    return obj


@app.put('/api/courses/{cid}', response_model=CourseOut, tags=['Courses'])
async def replace_course(cid: int, payload: CourseIn, db: AsyncSession = Depends(get_db)):
    res = await db.execute(select(Course).where(Course.course_id == cid))
    obj = res.scalar_one_or_none()
    if not obj:
        raise HTTPException(status_code=404, detail='Course not found')
    for k, v in payload.dict().items():
        setattr(obj, k, v)
    await db.commit()
    await db.refresh(obj)
    return obj


@app.patch('/api/courses/{cid}', response_model=CourseOut, tags=['Courses'])
async def patch_course(cid: int, payload: CourseEdit, db: AsyncSession = Depends(get_db)):
    res = await db.execute(select(Course).where(Course.course_id == cid))
    obj = res.scalar_one_or_none()
    if not obj:
        raise HTTPException(status_code=404, detail='Course not found')
    for k, v in payload.dict(exclude_none=True).items():
        setattr(obj, k, v)
    await db.commit()
    await db.refresh(obj)
    return obj


@app.delete('/api/courses/{cid}', status_code=status.HTTP_204_NO_CONTENT, tags=['Courses'])
async def delete_course(cid: int, db: AsyncSession = Depends(get_db)):
    res = await db.execute(select(Course).where(Course.course_id == cid))
    obj = res.scalar_one_or_none()
    if not obj:
        raise HTTPException(status_code=404, detail='Course not found')
    await db.delete(obj)
    await db.commit()


@app.get('/api/courses/{cid}/students', response_model=List[StudentOut], tags=['Courses'])
async def course_students(cid: int, db: AsyncSession = Depends(get_db)):
    res = await db.execute(select(Course).where(Course.course_id == cid))
    if not res.scalar_one_or_none():
        raise HTTPException(status_code=404, detail='Course not found')
    qry = (
        select(Student)
        .join(Enrollment, Enrollment.stu_id == Student.stu_id)
        .where(Enrollment.course_id == cid)
    )
    stu_res = await db.execute(qry)
    return stu_res.scalars().all()


def dispatch_email(addr: str):
    print(f'Sending enrollment confirmation to {addr}')


@app.post('/api/enrollments/', response_model=EnrollOut, status_code=status.HTTP_201_CREATED, tags=['Enrollments'])
async def enroll_student(payload: EnrollIn, bg: BackgroundTasks, db: AsyncSession = Depends(get_db)):
    stu_res = await db.execute(select(Student).where(Student.stu_id == payload.stu_id))
    stu = stu_res.scalar_one_or_none()
    if not stu:
        raise HTTPException(status_code=404, detail='Student not found')

    entry = Enrollment(stu_id=payload.stu_id, course_id=payload.course_id)
    db.add(entry)
    await db.commit()
    await db.refresh(entry)

    bg.add_task(dispatch_email, stu.email_addr)
    return entry


@app.get('/api/students/', response_model=List[StudentOut], tags=['Students'])
async def list_students(db: AsyncSession = Depends(get_db)):
    res = await db.execute(select(Student))
    return res.scalars().all()


@app.post('/api/students/', response_model=StudentOut, status_code=status.HTTP_201_CREATED, tags=['Students'])
async def create_student(payload: StudentIn, db: AsyncSession = Depends(get_db)):
    obj = Student(**payload.dict())
    db.add(obj)
    await db.commit()
    await db.refresh(obj)
    return obj
