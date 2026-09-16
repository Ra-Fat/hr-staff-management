from datetime import date, datetime, timezone

from sqlalchemy import Column, Date, DateTime, ForeignKey, Index, Integer, Numeric, String, text
from sqlalchemy import Enum as SqlEnum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy.schema import UniqueConstraint

from app.core.database import Base
from app.core.utils import generate_uuid
from app.core.enum import StaffStatus


class Staff(Base):
    __tablename__ = "staff"

    id = Column(Integer, primary_key=True, index=True)
    uuid = Column(
        UUID(as_uuid=True),
        server_default=func.gen_random_uuid(),  
        default=generate_uuid,                   
        unique=True,
        index=True,
        nullable=False,                          
    )

    user_id = Column(Integer, ForeignKey("auth_accounts.id", ondelete="SET NULL"), nullable=True)
    department_id = Column(Integer, ForeignKey("departments.id"), nullable=True)
    position_id = Column(Integer, ForeignKey("positions.id"), nullable=True)

    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    hire_date = Column(Date, nullable=True)
    salary = Column(Numeric(12, 2), nullable=True)

    profile_url = Column(String(500), nullable=True)

    status = Column(SqlEnum(StaffStatus, name="staff_status_enum"), nullable=False, default=StaffStatus.ACTIVE)

    auth_account = relationship("AdminUser", back_populates="staff_profile", lazy="selectin")
    position_obj = relationship("Position", back_populates="staff", lazy="selectin")
    department = relationship("Department", back_populates="staff", lazy="selectin")

    # leave_requests = relationship("LeaveRequest", back_populates="staff", lazy="noload")
    attendance_records = relationship("Attendance", back_populates="staff", lazy="noload")

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    deleted_at = Column(DateTime(timezone=True), nullable=True, default=None)

    __table_args__ = (
        Index("idx_staff_user_id", "user_id"),
        Index("idx_staff_department_id", "department_id"),
        Index("idx_staff_status", "status"),
        Index("idx_staff_position_id", "position_id"),
        UniqueConstraint("uuid"),
    )

    @property
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}" 