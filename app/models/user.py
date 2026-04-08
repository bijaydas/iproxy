from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.enums import UserStatus

if TYPE_CHECKING:
    from app.models.session import Session


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    name: Mapped[str] = mapped_column(String(30), nullable=True)
    email: Mapped[str] = mapped_column(String(30), unique=True, nullable=False)
    password: Mapped[str]

    """Based upon this status user will be able to log in"""
    status: Mapped[str] = mapped_column(String(30), default=UserStatus.active.value)

    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now(), onupdate=datetime.now())

    """This is soft delete"""
    is_deleted: Mapped[int] = mapped_column(Integer, default=0)

    sessions: Mapped[list["Session"]] = relationship("Session", back_populates="user")
