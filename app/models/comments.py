from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Text, ForeignKey

from app.db import Base
from app.models.mixins import IDMixin, TimestampMixin


class CommentsOrm(Base, IDMixin, TimestampMixin):
    __tablename__ = "comments"

    content: Mapped[str] = mapped_column(Text(), nullable=False)
    likes_count: Mapped[int] = mapped_column(nullable=False, default=0)

    user_id: Mapped[int | None] = mapped_column(
        ForeignKey("users.id", ondelete="SET NULL"), nullable=True
    )
    post_id: Mapped[int] = mapped_column(
        ForeignKey("posts.id", ondelete="CASCADE"), nullable=False
    )

    author: Mapped['UsersOrm'] = relationship('UsersOrm', back_populates='comments')
    post: Mapped['PostsOrm'] = relationship('PostOrm', back_populates='comments')
