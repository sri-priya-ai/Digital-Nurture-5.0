from fastapi import FastAPI, Depends, HTTPException, status, Request
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, or_
from typing import Optional, List

from database import get_db, async_eng, Base
from db_models import Course
from schemas import CourseIn, CourseEdit, CourseOut

app = FastAPI(
    title='Course Management API v1',
    description='RESTful Course Management — versioned, paginated, standardised errors.',
    version='1.0.0',
)

# URL versioning chosen over header versioning because:
#   - /api/v1/... is immediately visible in browser and curl
#   - Header versioning (Accept: application/vnd.api+json;version=1) keeps
#     URLs clean but is harder to test and cache
#   Trade-off: URL versioning creates parallel URL trees when v2 ships


@app.on_event('startup')
async def boot():
    async with async_eng.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


def err_body(code: str, msg: str, field=None):
    return {'error': {'code': code, 'message': msg, 'field': field}}


@app.exception_handler(404)
async def handle_404(req: Request, exc):
    return JSONResponse(status_code=404, content=err_body('NOT_FOUND', 'Resource not found'))


@app.exception_handler(500)
async def handle_500(req: Request, exc):
    return JSONResponse(status_code=500, content=err_body('SERVER_ERROR', 'Unexpected server error'))


@app.get('/api/v1/courses/', tags=['Courses v1'])
async def list_courses(
    page: int = 1,
    page_size: int = 10,
    search: Optional[str] = None,
    db: AsyncSession = Depends(get_db)
):
    offset_val = (page - 1) * page_size

    base_qry = select(Course)
    if search:
        term = f'%{search}%'
        base_qry = base_qry.where(
            or_(Course.course_title.ilike(term), Course.course_code.ilike(term))
        )

    total_res = await db.execute(select(func.count()).select_from(base_qry.subquery()))
    total_count = total_res.scalar()

    rows_res = await db.execute(base_qry.offset(offset_val).limit(page_size))
    rows = rows_res.scalars().all()

    base_url = f'/api/v1/courses/?page_size={page_size}'
    nxt = f'{base_url}&page={page + 1}' if offset_val + page_size < total_count else None
    prv = f'{base_url}&page={page - 1}' if page > 1 else None

    return {
        'count': total_count,
        'next': nxt,
        'previous': prv,
        'results': [CourseOut.from_orm(r) for r in rows],
    }


@app.post('/api/v1/courses/', response_model=CourseOut, status_code=status.HTTP_201_CREATED, tags=['Courses v1'])
async def create_course(payload: CourseIn, request: Request, db: AsyncSession = Depends(get_db)):
    obj = Course(**payload.dict())
    db.add(obj)
    await db.commit()
    await db.refresh(obj)

    resp = JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content=CourseOut.from_orm(obj).dict(),
    )
    resp.headers['Location'] = f'/api/v1/courses/{obj.course_id}/'
    return resp


@app.get('/api/v1/courses/{cid}/', response_model=CourseOut, tags=['Courses v1'])
async def get_course(cid: int, db: AsyncSession = Depends(get_db)):
    res = await db.execute(select(Course).where(Course.course_id == cid))
    obj = res.scalar_one_or_none()
    if not obj:
        raise HTTPException(
            status_code=404,
            detail=err_body('NOT_FOUND', f'Course with id {cid} does not exist'),
        )
    return obj


@app.put('/api/v1/courses/{cid}/', response_model=CourseOut, tags=['Courses v1'])
async def replace_course(cid: int, payload: CourseIn, db: AsyncSession = Depends(get_db)):
    res = await db.execute(select(Course).where(Course.course_id == cid))
    obj = res.scalar_one_or_none()
    if not obj:
        raise HTTPException(
            status_code=404,
            detail=err_body('NOT_FOUND', f'Course with id {cid} does not exist'),
        )
    for k, v in payload.dict().items():
        setattr(obj, k, v)
    await db.commit()
    await db.refresh(obj)
    return obj


@app.patch('/api/v1/courses/{cid}/', response_model=CourseOut, tags=['Courses v1'])
async def patch_course(cid: int, payload: CourseEdit, db: AsyncSession = Depends(get_db)):
    res = await db.execute(select(Course).where(Course.course_id == cid))
    obj = res.scalar_one_or_none()
    if not obj:
        raise HTTPException(
            status_code=404,
            detail=err_body('NOT_FOUND', f'Course with id {cid} does not exist'),
        )
    for k, v in payload.dict(exclude_none=True).items():
        setattr(obj, k, v)
    await db.commit()
    await db.refresh(obj)
    return obj


@app.delete('/api/v1/courses/{cid}/', status_code=status.HTTP_204_NO_CONTENT, tags=['Courses v1'])
async def remove_course(cid: int, db: AsyncSession = Depends(get_db)):
    res = await db.execute(select(Course).where(Course.course_id == cid))
    obj = res.scalar_one_or_none()
    if not obj:
        raise HTTPException(
            status_code=404,
            detail=err_body('NOT_FOUND', f'Course with id {cid} does not exist'),
        )
    await db.delete(obj)
    await db.commit()
