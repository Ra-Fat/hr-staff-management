from datetime import date, datetime, timezone

from sqlalchemy import Column, Date, DateTime, ForeignKey, Index, Integer, text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy.schema import UniqueConstraint
from app.core.utils import generate_uuid


from app.core.database import Base


class Attendance(Base):
    __tablename__ = "attendance"

    id = Column(Integer, primary_key=True, index=True)
    uuid = Column(UUID(as_uuid=True), default=generate_uuid, unique=True, index=True)
    
    staff_id = Column(Integer, ForeignKey("staff.id", ondelete="CASCADE"), nullable=False)
    check_in = Column(DateTime(timezone=True), nullable=True)
    check_out = Column(DateTime(timezone=True), nullable=True)
    date = Column(Date, nullable=False)

    staff = relationship("Staff", back_populates="attendance_records", lazy="selectin")

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    deleted_at = Column(DateTime(timezone=True), nullable=True, default=None)

    __table_args__ = (
        Index("idx_attendance_staff_id", "staff_id"),
        Index("idx_attendance_date", "date"),
        UniqueConstraint("uuid"),
        Index("idx_attendance_staff_date", "staff_id", "date", unique=True),
    )