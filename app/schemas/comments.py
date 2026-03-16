from pydantic import BaseModel, Field, ConfigDict

from datetime import datetime


class CommentAdd(BaseModel):
    content: str
    user_id: int
    post_id: int

class CommentGet(CommentAdd):
    id: int
    likes_count: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
    
class CommentUpdate(BaseModel):
    content: str | None = None
    likes_count: int | None = None
