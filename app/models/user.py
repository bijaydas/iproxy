from datetime import datetime

from sqlalchemy import String, Integer, DateTime
from sqlalchemy.orm import mapped_column, Mapped

from app.core.database import Base
from app.enums import UserStatus


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    email: Mapped[str] = mapped_column(String(30), unique=True, nullable=False)
    password: Mapped[str]

    """Based upon this status user will be able to log in"""
    status: Mapped[str] = mapped_column(String(30), default=UserStatus.active.value)

    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now(), onupdate=datetime.now())

    """This is soft delete"""
    is_deleted: Mapped[int] = mapped_column(Integer, default=0)
