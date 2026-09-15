from sqlalchemy import Column, DateTime, Index, Integer, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy.schema import UniqueConstraint

from app.core.database import Base
from app.core.utils import generate_uuid


class Position(Base):
    __tablename__ = "positions"

    id = Column(Integer, primary_key=True, index=True)
    uuid = Column(
        UUID(as_uuid=True),
        server_default=func.gen_random_uuid(),
        default=generate_uuid,
        unique=True,
        index=True,
        nullable=False,
    )

    title = Column(String(150), nullable=False, unique=True)
    description = Column(String(500), nullable=True)

    staff = relationship("Staff", back_populates="position_obj", lazy="noload")

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    deleted_at = Column(DateTime(timezone=True), nullable=True, default=None)

    __table_args__ = (
        Index("idx_positions_title", "title"),
    )