import datetime
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.db import Base, TimestampMixin

# from app.users.models import User


class Token(Base, TimestampMixin):
    __tablename__ = "token"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, index=True)
    token: Mapped[str] = mapped_column(index=True)
    expiry: Mapped[datetime.datetime] = mapped_column()
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))

    user: Mapped["User"] = relationship("User", back_populates="tokens")  # noqa
