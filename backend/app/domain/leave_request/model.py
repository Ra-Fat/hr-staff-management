from datetime import date, datetime, timezone

from sqlalchemy import Column, Date, DateTime, ForeignKey, Index, Integer, String, text
from sqlalchemy import Enum as SqlEnum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.utils import generate_uuid

from app.core.database import Base
from app.core.enum import LeaveStatus, LeaveType
from sqlalchemy.schema import UniqueConstraint



class LeaveRequest(Base):
    __tablename__ = "leave_requests"

    id = Column(Integer, primary_key=True, index=True)
    uuid = Column(
        UUID(as_uuid=True),
        server_default=func.gen_random_uuid(),  
        default=generate_uuid,                   
        unique=True,
        index=True,
        nullable=False,                          
    )
    

    staff_id = Column(Integer, ForeignKey("staff.id", ondelete="CASCADE"), nullable=False)
    leave_type = Column(SqlEnum(LeaveType, name="leave_type_enum"), nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    status = Column(SqlEnum(LeaveStatus, name="leave_status_enum"), nullable=False, default=LeaveStatus.PENDING)
    reviewed_by = Column(Integer, ForeignKey("auth_accounts.id", ondelete="SET NULL"), nullable=True)

    staff = relationship("Staff", back_populates="leave_requests", lazy="selectin")
    reviewed_by_user = relationship("AuthAccount", lazy="selectin")

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    deleted_at = Column(DateTime(timezone=True), nullable=True, default=None)

    
    __table_args__ = (
        Index("idx_leave_requests_staff_id", "staff_id"),
        Index("idx_leave_requests_status", "status"),
        UniqueConstraint("uuid"),
        Index("idx_leave_requests_staff_status", "staff_id", "status"),
    )