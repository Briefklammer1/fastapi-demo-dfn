from typing import List
from sqlalchemy.orm import backref, relationship
from sqlalchemy.orm.relationships import foreign
from sqlalchemy.sql.expression import null, text

from app.schemas import PostBase
from .database import Base
from sqlalchemy import Column, Integer, String, Boolean, TIMESTAMP, ForeignKey

class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, server_default="TRUE", nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=text("now()"), nullable=False)
    creator_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    creator = relationship("User")

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password= Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("now()"))

class Vote(Base):
    __tablename__ = "votes"

    post_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    user_id = Column(Integer, ForeignKey("posts.id", ondelete="CASCADE"), primary_key=True)