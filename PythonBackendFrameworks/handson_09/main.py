from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from jose import JWTError
from typing import List

from database import get_db, async_eng, Base
from db_models import Course, AppUser
from schemas import CourseIn, CourseOut
from auth_schemas import RegisterIn, LoginIn, TokenOut, UserOut
from security import hash_pwd, check_pwd, build_token, decode_token

app = FastAPI(title='Course Management API — Secured', version='1.0')

app.add_middleware(
    CORSMiddleware,
    allow_origins=['http://localhost:3000'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

oauth2_bearer = OAuth2PasswordBearer(tokenUrl='/api/v1/auth/login/')

# OAuth2 Authorization Code flow vs simple JWT login:
#   Simple JWT login (what we implemented):
#     - Client sends credentials directly to our API
#     - API returns a token
#     - Good for first-party apps (you own both frontend and backend)
#
#   OAuth2 Authorization Code flow:
#     - User is redirected to an authorization server (e.g. Google, GitHub)
#     - Auth server issues a short-lived code back to the client's redirect URL
#     - Client exchanges that code (server-side) for an access token + refresh token
#     - Good for third-party integrations where you don't want users sharing passwords


@app.on_event('startup')
async def boot():
    async with async_eng.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def get_current_user(token: str = Depends(oauth2_bearer), db: AsyncSession = Depends(get_db)):
    cred_err = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Invalid or expired token',
        headers={'WWW-Authenticate': 'Bearer'},
    )
    try:
        claims = decode_token(token)
        uid = claims.get('sub')
        if not uid:
            raise cred_err
    except JWTError:
        raise cred_err

    res = await db.execute(select(AppUser).where(AppUser.user_id == int(uid)))
    usr = res.scalar_one_or_none()
    if not usr:
        raise cred_err
    return usr


@app.post('/api/v1/auth/register/', response_model=UserOut, status_code=status.HTTP_201_CREATED, tags=['Auth'])
async def register(payload: RegisterIn, db: AsyncSession = Depends(get_db)):
    existing = await db.execute(select(AppUser).where(AppUser.email_addr == payload.email_addr))
    if existing.scalar_one_or_none():
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='Email already registered')

    usr = AppUser(
        email_addr=payload.email_addr,
        pwd_hash=hash_pwd(payload.password),
    )
    db.add(usr)
    await db.commit()
    await db.refresh(usr)
    return usr


@app.post('/api/v1/auth/login/', response_model=TokenOut, tags=['Auth'])
async def login(payload: LoginIn, db: AsyncSession = Depends(get_db)):
    res = await db.execute(select(AppUser).where(AppUser.email_addr == payload.email_addr))
    usr = res.scalar_one_or_none()

    if not usr or not check_pwd(payload.password, usr.pwd_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid credentials')

    tok = build_token({'sub': str(usr.user_id)})
    return {'access_token': tok, 'token_type': 'bearer'}


@app.get('/api/v1/courses/', response_model=List[CourseOut], tags=['Courses'])
async def list_courses(db: AsyncSession = Depends(get_db)):
    res = await db.execute(select(Course))
    return res.scalars().all()


@app.post('/api/v1/courses/', response_model=CourseOut, status_code=status.HTTP_201_CREATED, tags=['Courses'])
async def create_course(
    payload: CourseIn,
    db: AsyncSession = Depends(get_db),
    curr_user: AppUser = Depends(get_current_user),
):
    obj = Course(**payload.dict())
    db.add(obj)
    await db.commit()
    await db.refresh(obj)
    return obj


@app.delete('/api/v1/courses/{cid}/', status_code=status.HTTP_204_NO_CONTENT, tags=['Courses'])
async def remove_course(
    cid: int,
    db: AsyncSession = Depends(get_db),
    curr_user: AppUser = Depends(get_current_user),
):
    res = await db.execute(select(Course).where(Course.course_id == cid))
    obj = res.scalar_one_or_none()
    if not obj:
        raise HTTPException(status_code=404, detail='Course not found')
    await db.delete(obj)
    await db.commit()
