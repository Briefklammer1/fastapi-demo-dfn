from typing import Optional
from pydantic import BaseModel, EmailStr
from datetime import datetime

from pydantic.types import conint

#####Message######

class Message(BaseModel):
    message: str

#####User####

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode = True

class UserLogin(BaseModel):
    email: EmailStr
    password: str

####Post######

class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

class PostCreate(PostBase):
    pass

class PostUpdate(PostBase):
    title: str
    content: str
    published: bool

class PostResponse(PostBase):
    id: int
    created_at: datetime
    creator_id: int
    creator: UserResponse

    class Config:
        orm_mode = True

class PostGet(BaseModel):
    Post: PostResponse
    votes: int

    class Config:
        orm_mode = True


####Token####

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str]

#####Vote#####

class Vote(BaseModel):
    post_id: int
    dir: conint(ge=0, le=1)
    