from sqlalchemy.orm import Mapped, mapped_column

from app.core.db import Base, TimestampMixin
from sqlalchemy.orm import relationship

from app.auth.models import Token


class User(Base, TimestampMixin):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, index=True)
    username: Mapped[str] = mapped_column(index=True)
    email: Mapped[str] = mapped_column(index=True, unique=True)
    hashed_password: Mapped[str] = mapped_column()
    is_active: Mapped[bool] = mapped_column()
    is_superuser: Mapped[bool] = mapped_column(default=False)
    tokens: Mapped[list["Token"] | None] = relationship(back_populates="user")
