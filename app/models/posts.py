from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Text, ForeignKey

from app.db import Base
from app.models.mixins import IDMixin, TimestampMixin


class PostsOrm(Base, IDMixin, TimestampMixin):
    __tablename__ = 'posts'

    title: Mapped[str] = mapped_column(String(100), nullable=False)
    content: Mapped[str] = mapped_column(Text(), nullable=False)

    views_count: Mapped[int] = mapped_column(nullable=False, default=0)
    likes_count: Mapped[int] = mapped_column(nullable=False, default=0)

    user_id: Mapped[int | None] = mapped_column(
        ForeignKey('users.id', ondelete='SET NULL'), nullable=True, default=None
    )

    user: Mapped['UsersOrm'] = relationship('UsersOrm', back_populates='posts')
    comments: Mapped[list['CommentsOrm']] = relationship('CommentsOrm', back_populates='post')
