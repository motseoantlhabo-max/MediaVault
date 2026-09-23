import os
from fastapi import APIRouter, Depends, status, UploadFile, File, Form, BackgroundTasks, HTTPException
from fastapi.responses import FileResponse
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional
from app.core.database import get_db
from app.core.dependencies import get_current_user, require_creator_or_admin
from app.core.asset_dependencies import check_asset_ownership, check_asset_access
from app.models.user import User
from app.models.media_asset import MediaAsset
from app.schemas.media_asset import (
    MediaAssetCreate,
    MediaAssetUpdate,
    MediaAssetResponse,
    MediaAssetListResponse,
    AssetUploadResponse
)
from app.schemas.comment import CommentCreate, CommentResponse
from app.services.file_service import validate_file_size, validate_mime_type, save_upload_file
from app.services.asset_service import (
    create_media_asset,
    get_media_assets,
    get_media_asset,
    update_media_asset,
    delete_media_asset
)
from app.core.config import get_settings

settings = get_settings()

router = APIRouter()


@router.post("/upload", response_model=AssetUploadResponse, status_code=status.HTTP_201_CREATED)
async def upload_asset(
    file: UploadFile = File(...),
    title: str = Form(...),
    current_user: User = Depends(require_creator_or_admin),
    db: AsyncSession = Depends(get_db),
    background_tasks: BackgroundTasks = BackgroundTasks()
):
    """Upload a media file and spawn background OCR processing."""
    # Validate file
    await validate_file_size(file)
    await validate_mime_type(file)
    
    # Save file
    file_path, filename = await save_upload_file(file, settings.UPLOAD_DIR)
    
    # Create asset record
    asset_data = MediaAssetCreate(title=title)
    asset = await create_media_asset(
        asset_data=asset_data,
        file_path=file_path,
        mime_type=file.content_type,
        owner_id=current_user.id,
        db=db,
        background_tasks=background_tasks
    )
    
    return AssetUploadResponse(
        id=asset.id,
        title=asset.title,
        file_path=asset.file_path,
        mime_type=asset.mime_type,
        status=asset.status,
        message="File uploaded successfully. Processing started."
    )


@router.get("", response_model=list[MediaAssetListResponse])
async def list_assets(
    skip: int = 0,
    limit: int = 100,
    tag: Optional[str] = None,
    mime_type: Optional[str] = None,
    ocr_search: Optional[str] = None,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """List all media assets with filtering and pagination."""
    assets = await get_media_assets(
        db=db,
        skip=skip,
        limit=limit,
        tag=tag,
        mime_type=mime_type,
        ocr_search=ocr_search
    )
    
    return [
        MediaAssetListResponse(
            id=asset.id,
            title=asset.title,
            mime_type=asset.mime_type,
            status=asset.status,
            owner_id=asset.owner_id
        )
        for asset in assets
    ]


@router.get("/{asset_id}", response_model=MediaAssetResponse)
async def get_asset(
    asset: MediaAsset = Depends(check_asset_access)
):
    """Get detailed information about a specific asset including OCR text and comments."""
    return MediaAssetResponse(
        id=asset.id,
        title=asset.title,
        file_path=asset.file_path,
        mime_type=asset.mime_type,
        ocr_text=asset.ocr_text,
        status=asset.status,
        owner_id=asset.owner_id
    )


@router.get("/{asset_id}/stream")
async def stream_asset(
    asset: MediaAsset = Depends(check_asset_access)
):
    """Stream the binary file content with range header support."""
    if not os.path.exists(asset.file_path):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="File not found on disk"
        )
    
    return FileResponse(
        path=asset.file_path,
        media_type=asset.mime_type,
        filename=f"{asset.title}.{asset.mime_type.split('/')[-1]}"
    )


@router.delete("/{asset_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_asset(
    asset: MediaAsset = Depends(check_asset_ownership),
    db: AsyncSession = Depends(get_db)
):
    """Delete an asset and its physical file."""
    success = await delete_media_asset(asset.id, db)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Asset not found"
        )


@router.post("/{asset_id}/comments", response_model=CommentResponse, status_code=status.HTTP_201_CREATED)
async def add_comment(
    asset: MediaAsset = Depends(check_asset_access),
    content: str = Form(...),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Add a comment to an asset."""
    from app.models.asset_comment import AssetComment
    import uuid
    
    new_comment = AssetComment(
        id=str(uuid.uuid4()),
        content=content,
        asset_id=asset.id,
        user_id=current_user.id
    )
    
    db.add(new_comment)
    await db.commit()
    await db.refresh(new_comment)
    
    return CommentResponse(
        id=new_comment.id,
        content=new_comment.content,
        asset_id=new_comment.asset_id,
        user_id=new_comment.user_id
    )
