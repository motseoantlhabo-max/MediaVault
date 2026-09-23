from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.schemas.user import UserCreate, UserResponse, UserLogin, Token
from app.services.auth_service import create_user, authenticate_user, create_tokens_for_user

router = APIRouter()


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(user_data: UserCreate, db: AsyncSession = Depends(get_db)):
    """Register a new user with default Creator role."""
    user = await create_user(user_data, db)
    return user


@router.post("/login", response_model=Token)
async def login(user_credentials: UserLogin, db: AsyncSession = Depends(get_db)):
    """Authenticate user and return JWT tokens."""
    user = await authenticate_user(user_credentials.email, user_credentials.password, db)
    tokens = await create_tokens_for_user(user)
    return tokens
