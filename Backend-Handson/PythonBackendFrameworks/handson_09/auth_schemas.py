from pydantic import BaseModel, EmailStr


class RegisterIn(BaseModel):
    email_addr: EmailStr
    password: str


class LoginIn(BaseModel):
    email_addr: EmailStr
    password: str


class TokenOut(BaseModel):
    access_token: str
    token_type: str = 'bearer'


class UserOut(BaseModel):
    user_id: int
    email_addr: str
    is_active: int

    class Config:
        from_attributes = True
