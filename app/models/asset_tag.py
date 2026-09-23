from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from app.core.database import Base


class AssetTag(Base):
    __tablename__ = "asset_tags"
    
    asset_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("media_assets.id", ondelete="CASCADE"),
        primary_key=True
    )
    tag_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("tags.id", ondelete="CASCADE"),
        primary_key=True
    )
