from pydantic import BaseModel, Field
from typing import Optional


class CommentBase(BaseModel):
    content: str = Field(..., min_length=1)


class CommentCreate(CommentBase):
    asset_id: str


class CommentResponse(BaseModel):
    id: str
    content: str
    asset_id: str
    user_id: str

    class Config:
        from_attributes = True
