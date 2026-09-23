from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_
from typing import Optional, List
from fastapi import BackgroundTasks
from app.models.media_asset import MediaAsset
from app.schemas.media_asset import MediaAssetCreate, MediaAssetUpdate
from app.services.ocr_service import extract_text_from_image, extract_text_from_pdf
from app.services.file_service import delete_file
import os


async def create_media_asset(
    asset_data: MediaAssetCreate,
    file_path: str,
    mime_type: str,
    owner_id: str,
    db: AsyncSession,
    background_tasks: BackgroundTasks
) -> MediaAsset:
    new_asset = MediaAsset(
        title=asset_data.title,
        file_path=file_path,
        mime_type=mime_type,
        status="pending",
        owner_id=owner_id
    )
    
    db.add(new_asset)
    await db.commit()
    await db.refresh(new_asset)
    
    # Schedule background processing
    background_tasks.add_task(process_asset_background, new_asset.id, db)
    
    return new_asset


async def process_asset_background(asset_id: str, db: AsyncSession) -> None:
    """Background task to process uploaded assets (OCR, thumbnails, etc.)."""
    from app.core.database import AsyncSessionLocal
    
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(MediaAsset).where(MediaAsset.id == asset_id))
        asset = result.scalar_one_or_none()
        
        if not asset:
            return
        
        try:
            # Update status to PROCESSING
            asset.status = "processing"
            await session.commit()
            
            # Perform OCR based on file type
            if asset.mime_type in ["image/jpeg", "image/png"]:
                ocr_text = await extract_text_from_image(asset.file_path)
                if ocr_text:
                    asset.ocr_text = ocr_text
            elif asset.mime_type == "application/pdf":
                ocr_text = await extract_text_from_pdf(asset.file_path)
                if ocr_text:
                    asset.ocr_text = ocr_text
            
            # Update status to COMPLETED
            asset.status = "completed"
            await session.commit()
            
        except Exception as e:
            print(f"Error processing asset {asset_id}: {e}")
            asset.status = "failed"
            await session.commit()


async def get_media_assets(
    db: AsyncSession,
    skip: int = 0,
    limit: int = 100,
    tag: Optional[str] = None,
    mime_type: Optional[str] = None,
    ocr_search: Optional[str] = None
) -> List[MediaAsset]:
    query = select(MediaAsset)
    
    if tag:
        # Filter by tag (would require join with asset_tags table)
        pass
    
    if mime_type:
        query = query.where(MediaAsset.mime_type == mime_type)
    
    if ocr_search:
        query = query.where(MediaAsset.ocr_text.contains(ocr_search))
    
    query = query.offset(skip).limit(limit)
    result = await db.execute(query)
    return result.scalars().all()


async def get_media_asset(asset_id: str, db: AsyncSession) -> Optional[MediaAsset]:
    result = await db.execute(select(MediaAsset).where(MediaAsset.id == asset_id))
    return result.scalar_one_or_none()


async def update_media_asset(
    asset_id: str,
    asset_data: MediaAssetUpdate,
    db: AsyncSession
) -> Optional[MediaAsset]:
    result = await db.execute(select(MediaAsset).where(MediaAsset.id == asset_id))
    asset = result.scalar_one_or_none()
    
    if not asset:
        return None
    
    if asset_data.title is not None:
        asset.title = asset_data.title
    
    await db.commit()
    await db.refresh(asset)
    return asset


async def delete_media_asset(asset_id: str, db: AsyncSession) -> bool:
    result = await db.execute(select(MediaAsset).where(MediaAsset.id == asset_id))
    asset = result.scalar_one_or_none()
    
    if not asset:
        return False
    
    # Delete physical file
    await delete_file(asset.file_path)
    
    # Delete database record
    await db.delete(asset)
    await db.commit()
    
    return True
