import uuid
from sqlalchemy import String, Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base


class AssetComment(Base):
    __tablename__ = "asset_comments"
    
    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4())
    )
    content: Mapped[str] = mapped_column(Text, nullable=False)
    asset_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("media_assets.id", ondelete="CASCADE"),
        nullable=False
    )
    user_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False
    )
    
    # Relationships
    asset = relationship("MediaAsset", back_populates="comments")
    user = relationship("User", back_populates="comments")
