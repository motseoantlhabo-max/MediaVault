import uuid
from sqlalchemy import String, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base


class User(Base):
    __tablename__ = "users"
    
    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4())
    )
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    role: Mapped[str] = mapped_column(
        String(20),
        default="creator",
        nullable=False
    )
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    
    # Relationships
    media_assets = relationship("MediaAsset", back_populates="owner", cascade="all, delete-orphan")
    comments = relationship("AssetComment", back_populates="user", cascade="all, delete-orphan")
    audit_logs = relationship("AuditLog", back_populates="user", cascade="all, delete-orphan")
