from datetime import datetime, timezone

from sqlalchemy import Column, DateTime, ForeignKey, Index, Integer, String, text
from sqlalchemy import Enum as SqlEnum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.core.database import Base
from app.core.enum import AdminStatus

class AuthAccount(Base):
    __tablename__ = "auth_account"

    id = Column(Integer, primary_key= True, index= True)
    uuid = Column(
        UUID(as_uuid= True),
        nullable= False,
        unique= True,
        index= True,
        server_default=text("gen_random_uuid()"),
    )