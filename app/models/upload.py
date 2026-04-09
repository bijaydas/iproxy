from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.models import User


class Upload(Base):
    __tablename__ = "uploads"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))

    job_description_path: Mapped[str]
    resume_path: Mapped[str]

    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now())

    user: Mapped["User"] = relationship("User", back_populates="uploads")
