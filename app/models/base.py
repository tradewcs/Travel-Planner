from datetime import datetime
from sqlalchemy import DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, declared_attr
from advanced_alchemy.base import UUIDAuditBase
from advanced_alchemy.mixins import AuditColumnsMixin, SoftDeleteMixin


class BaseModel(UUIDAuditBase, AuditColumnsMixin, SoftDeleteMixin):
    """Base model with UUID PK, audit columns, and soft delete functionality."""

    __abstract__ = True

    @declared_attr
    def __tablename__(cls) -> str:
        """Generate table name automatically from class name."""
        return cls.__name__.lower() + "s"

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.current_timestamp(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.current_timestamp(),
        onupdate=func.current_timestamp(),
        nullable=False,
    )
