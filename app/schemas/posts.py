from pydantic import BaseModel, Field, ConfigDict

from datetime import datetime


class PostAdd(BaseModel):
    title: str = Field(max_length=100)
    content: str

    user_id: int

class PostGet(PostAdd):
    id: int
    views_count: int
    likes_count: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

class PostUpdate(BaseModel):
    title: str | None = Field(default=None, max_length=100)
    content: str | None = None
    views_count: int | None = None
    likes_count: int | None = None
    