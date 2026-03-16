from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Text, CheckConstraint

from app.models.mixins import IDMixin, TimestampMixin
from app.db import Base


class UsersOrm(Base, IDMixin, TimestampMixin):
    __tablename__ = 'users'

    first_name: Mapped[str] = mapped_column(String(50), nullable=False)
    last_name: Mapped[str] = mapped_column(String(50), nullable=False)
    age: Mapped[int] = mapped_column(
        CheckConstraint('age >= 16', name='chk_age'), nullable=False
    )

    bio: Mapped[str | None] = mapped_column(Text(), nullable=True, default=None)

    username: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)

    email: Mapped[str] = mapped_column(nullable=False, unique=True)
    phone: Mapped[str] = mapped_column(nullable=False, unique=True)

    is_active: Mapped[bool] = mapped_column(default=True)

    posts: Mapped[list['PostsOrm']] = relationship('PostsOrm', back_populates='user')
    comments: Mapped[list['CommentsOrm']] = relationship('CommentsOrm', back_populates='author')