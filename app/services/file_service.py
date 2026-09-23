import os
import uuid
import aiofiles
from pathlib import Path
from fastapi import UploadFile, HTTPException, status
from typing import Tuple
from app.core.config import get_settings

settings = get_settings()


async def validate_file_size(file: UploadFile) -> None:
    """Validate file size against maximum allowed size."""
    file_size = 0
    for chunk in file.file:
        file_size += len(chunk)
        if file_size > settings.MAX_FILE_SIZE_MB * 1024 * 1024:
            raise HTTPException(
                status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                detail=f"File size exceeds maximum allowed size of {settings.MAX_FILE_SIZE_MB}MB"
            )
    await file.seek(0)  # Reset file pointer


async def validate_mime_type(file: UploadFile) -> None:
    """Validate file MIME type against allowed types."""
    if file.content_type not in settings.ALLOWED_MIME_TYPES:
        raise HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail=f"File type {file.content_type} is not supported. Allowed types: {', '.join(settings.ALLOWED_MIME_TYPES)}"
        )


async def save_upload_file(file: UploadFile, upload_dir: str) -> Tuple[str, str]:
    """Save uploaded file to disk and return (file_path, filename)."""
    # Create upload directory if it doesn't exist
    Path(upload_dir).mkdir(parents=True, exist_ok=True)
    
    # Generate unique filename
    file_extension = Path(file.filename).suffix
    unique_filename = f"{uuid.uuid4()}{file_extension}"
    file_path = os.path.join(upload_dir, unique_filename)
    
    # Save file
    async with aiofiles.open(file_path, 'wb') as f:
        content = await file.read()
        await f.write(content)
    
    return file_path, unique_filename


async def delete_file(file_path: str) -> bool:
    """Delete file from disk."""
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
            return True
        return False
    except Exception as e:
        print(f"Error deleting file: {e}")
        return False
