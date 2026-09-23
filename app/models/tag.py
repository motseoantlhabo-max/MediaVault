import uuid
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base


class Tag(Base):
    __tablename__ = "tags"
    
    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4())
    )
    name: Mapped[str] = mapped_column(String(100), unique=True, index=True, nullable=False)
    
    # Relationships
    media_assets = relationship("MediaAsset", secondary="asset_tags", back_populates="tags")
