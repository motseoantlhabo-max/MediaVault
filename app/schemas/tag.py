from pydantic import BaseModel, Field


class TagBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)


class TagCreate(TagBase):
    pass


class TagResponse(BaseModel):
    id: str
    name: str

    class Config:
        from_attributes = True
