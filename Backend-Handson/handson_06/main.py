from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Optional, List

from database import get_db, async_eng, Base
from db_models import Course, Student, Enrollment
from schemas import CourseIn, CourseEdit, CourseOut

app = FastAPI(title='Course Management API', version='1.0')


@app.on_event('startup')
async def init_db():
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
    qry = qry.offset(skip).limit(limit)
    result = await db.execute(qry)
    return result.scalars().all()


@app.post('/api/courses/', response_model=CourseOut, status_code=status.HTTP_201_CREATED, tags=['Courses'])
async def create_course(payload: CourseIn, db: AsyncSession = Depends(get_db)):
    new_course = Course(**payload.dict())
    db.add(new_course)
    await db.commit()
    await db.refresh(new_course)
    return new_course


@app.get('/api/courses/{course_id}', response_model=CourseOut, tags=['Courses'])
async def get_course(course_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Course).where(Course.course_id == course_id))
    obj = result.scalar_one_or_none()
    if not obj:
        raise HTTPException(status_code=404, detail='Course not found')
    return obj


@app.put('/api/courses/{course_id}', response_model=CourseOut, tags=['Courses'])
async def replace_course(course_id: int, payload: CourseIn, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Course).where(Course.course_id == course_id))
    obj = result.scalar_one_or_none()
    if not obj:
        raise HTTPException(status_code=404, detail='Course not found')
    for k, v in payload.dict().items():
        setattr(obj, k, v)
    await db.commit()
    await db.refresh(obj)
    return obj


@app.delete('/api/courses/{course_id}', status_code=status.HTTP_204_NO_CONTENT, tags=['Courses'])
async def remove_course(course_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Course).where(Course.course_id == course_id))
    obj = result.scalar_one_or_none()
    if not obj:
        raise HTTPException(status_code=404, detail='Course not found')
    await db.delete(obj)
    await db.commit()
