import uuid
from sqlalchemy import String, Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base


class MediaAsset(Base):
    __tablename__ = "media_assets"
    
    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4())
    )
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    file_path: Mapped[str] = mapped_column(String(500), nullable=False)
    mime_type: Mapped[str] = mapped_column(String(100), nullable=False)
    ocr_text: Mapped[str] = mapped_column(Text, nullable=True)
    status: Mapped[str] = mapped_column(
        String(20),
        default="pending",
        nullable=False
    )
    owner_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False
    )
    
    # Relationships
    owner = relationship("User", back_populates="media_assets")
    comments = relationship("AssetComment", back_populates="asset", cascade="all, delete-orphan")
    tags = relationship("Tag", secondary="asset_tags", back_populates="media_assets")
