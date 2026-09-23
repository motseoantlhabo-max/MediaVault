from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.models.user import User
from app.models.media_asset import MediaAsset


async def check_asset_ownership(
    asset_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
) -> MediaAsset:
    result = await db.execute(select(MediaAsset).where(MediaAsset.id == asset_id))
    asset = result.scalar_one_or_none()
    
    if asset is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Asset not found"
        )
    
    if asset.owner_id != current_user.id and current_user.role != "superadmin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to access this asset"
        )
    
    return asset


async def check_asset_access(
    asset_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
) -> MediaAsset:
    result = await db.execute(select(MediaAsset).where(MediaAsset.id == asset_id))
    asset = result.scalar_one_or_none()
    
    if asset is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Asset not found"
        )
    
    # Owners and superadmins can access any asset
    if asset.owner_id == current_user.id or current_user.role == "superadmin":
        return asset
    
    # Viewers can only read
    if current_user.role == "viewer":
        return asset
    
    # Creators can only access their own assets
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="You do not have permission to access this asset"
    )
