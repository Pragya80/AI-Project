from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.sql import func
from app.database import Base

class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    prompt = Column(Text, nullable=True)   # Fix: this is missing in your DB
    content = Column(Text, nullable=False)
    hashtags = Column(String, nullable=True)
    status = Column(String, default="draft")  # draft, scheduled, posted
    scheduled_time = Column(DateTime, nullable=True)
    posted_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, server_default=func.now())

class Profile(Base):
    __tablename__ = "profiles"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    headline = Column(String, nullable=True)
    about = Column(Text, nullable=True)

class Analytics(Base):
    __tablename__ = "analytics"

    id = Column(Integer, primary_key=True, index=True)
    post_id = Column(Integer, nullable=False)
    likes = Column(Integer, default=0)
    comments = Column(Integer, default=0)
    shares = Column(Integer, default=0)
    impressions = Column(Integer, default=0)
    created_at = Column(DateTime, server_default=func.now())
