from pydantic import BaseModel, Field


class MediaAssetBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)


class MediaAssetCreate(MediaAssetBase):
    pass


class MediaAssetUpdate(BaseModel):
    title: str | None = Field(None, min_length=1, max_length=255)


class MediaAssetResponse(BaseModel):
    id: str
    title: str
    file_path: str
    mime_type: str
    ocr_text: str | None = None
    status: str
    owner_id: str

    class Config:
        from_attributes = True


class MediaAssetListResponse(BaseModel):
    id: str
    title: str
    mime_type: str
    status: str
    owner_id: str

    class Config:
        from_attributes = True


class AssetUploadResponse(BaseModel):
    id: str
    title: str
    file_path: str
    mime_type: str
    status: str
    message: str = "File uploaded successfully. Processing started."

    class Config:
        from_attributes = True
