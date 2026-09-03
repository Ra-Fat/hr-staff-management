from sqlalchemy import Column, Date, DateTime, ForeignKey, Index, Integer, text, String

from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.core.database import Base
from sqlalchemy.schema import UniqueConstraint
from app.core.utils import generate_uuid


class Department(Base):
    __tablename__ = "departments"

    id = Column(Integer, primary_key=True, index=True)
    uuid = Column(
        UUID(as_uuid=True),
        server_default=func.gen_random_uuid(),  
        default=generate_uuid,                   
        unique=True,
        index=True,
        nullable=False,                          
    )
    
    name = Column(String(191), nullable=False, unique=True)
    staff = relationship("Staff", back_populates="department", lazy="noload")

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    deleted_at = Column(DateTime(timezone=True), nullable=True, default=None)

    __table_args__ = (
        Index("idx_departments_name", "name"),
        UniqueConstraint("uuid"),
    )