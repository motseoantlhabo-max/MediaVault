from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List
from app.core.database import get_db
from app.core.dependencies import require_superadmin
from app.models.user import User
from app.schemas.user import UserResponse, UserUpdate

router = APIRouter()


@router.get("", response_model=List[UserResponse])
async def list_users(
    current_user: User = Depends(require_superadmin),
    db: AsyncSession = Depends(get_db)
):
    """List all users (SuperAdmin only)."""
    result = await db.execute(select(User))
    users = result.scalars().all()
    
    return [
        UserResponse(
            id=user.id,
            email=user.email,
            role=user.role,
            is_active=user.is_active
        )
        for user in users
    ]


@router.get("/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: str,
    current_user: User = Depends(require_superadmin),
    db: AsyncSession = Depends(get_db)
):
    """Get a specific user (SuperAdmin only)."""
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    
    if not user:
        from fastapi import HTTPException
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    return UserResponse(
        id=user.id,
        email=user.email,
        role=user.role,
        is_active=user.is_active
    )


@router.patch("/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: str,
    user_data: UserUpdate,
    current_user: User = Depends(require_superadmin),
    db: AsyncSession = Depends(get_db)
):
    """Update a user (SuperAdmin only)."""
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    
    if not user:
        from fastapi import HTTPException
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    if user_data.email is not None:
        user.email = user_data.email
    if user_data.role is not None:
        user.role = user_data.role
    if user_data.is_active is not None:
        user.is_active = user_data.is_active
    
    await db.commit()
    await db.refresh(user)
    
    return UserResponse(
        id=user.id,
        email=user.email,
        role=user.role,
        is_active=user.is_active
    )
