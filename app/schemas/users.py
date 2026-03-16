from pydantic import BaseModel, Field, ConfigDict, EmailStr

from datetime import datetime

from app.schemas.posts import PostGet
from app.schemas.comments import CommentGet


class UserAdd(BaseModel):
    first_name: str = Field(max_length=50)
    last_name: str = Field(max_length=50)
    age: int = Field(ge=16)
    bio: str | None = Field(None)
    username: str = Field(max_length=50, description='Username пользователя должен быть уникальным', examples=['ivan_ivanov'])
    email: EmailStr = Field(description='Email пользователя должен быть уникальным', examples=['ivan@mail.ru'])
    phone: str = Field(description='Телефон должен быть уникальным', examples=['+79991234567'])

class UserGet(UserAdd):
    id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

class UserUpdate(BaseModel):
    first_name: str | None = Field(default=None, max_length=50)
    last_name: str | None = Field(default=None, max_length=50)
    age: int | None = Field(ge=16)
    bio: str | None = None
    username: str | None = Field(None, max_length=50, description='Username пользователя должен быть уникальным', examples=['ivan_ivanov'])
    email: EmailStr | None = Field(None, description='Email пользователя должен быть уникальным', examples=['ivan@mail.ru'])
    phone: str | None = Field(None, description='Телефон должен быть уникальным', examples=['+79991234567'])

class UserGetDTO(UserGet):
    posts: list[PostGet]
    comments: list[CommentGet]
    
UserGetDTO.model_rebuild()