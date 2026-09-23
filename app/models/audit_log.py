import uuid
from sqlalchemy import String, Text, ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import func
from app.core.database import Base


class AuditLog(Base):
    __tablename__ = "audit_logs"
    
    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4())
    )
    action: Mapped[str] = mapped_column(String(100), nullable=False)
    resource_type: Mapped[str] = mapped_column(String(100), nullable=False)
    resource_id: Mapped[str] = mapped_column(String(36), nullable=True)
    details: Mapped[str] = mapped_column(Text, nullable=True)
    user_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True
    )
    created_at: Mapped[str] = mapped_column(
        DateTime,
        server_default=func.now(),
        nullable=False
    )
    
    # Relationships
    user = relationship("User", back_populates="audit_logs")
