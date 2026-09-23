from pydantic import BaseModel, EmailStr, Field


class UserBase(BaseModel):
    email: EmailStr
    role: str = "creator"


class UserCreate(UserBase):
    password: str = Field(..., min_length=8)


class UserUpdate(BaseModel):
    email: EmailStr | None = None
    role: str | None = None
    is_active: bool | None = None


class UserResponse(BaseModel):
    id: str
    email: str
    role: str
    is_active: bool

    class Config:
        from_attributes = True


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    user_id: str | None = None
    email: str | None = None
    role: str | None = None
