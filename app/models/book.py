from sqlalchemy import Column, Integer, String
from app.db.db import Base
from pydantic import BaseModel, ConfigDict
from sqlalchemy.orm import relationship

class Book(Base):
    __tablename__ = "books"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    author = Column(String, nullable=False)
    year = Column(Integer, nullable=False)
    description = Column(String, nullable=True)

    # Relationship with reviews
    reviews = relationship("Review", back_populates="book", cascade="all, delete-orphan")

# Pydantic Models for Request/Response
class BookBase(BaseModel):
    title: str
    author: str
    year: int
    description: str | None = None

class BookInfo(BookBase):
    pass

class ChromaBookInfo(BaseModel):
    id: str
    title: str
    description: str | None = None


class BookResponse(BookBase):
    # Convert from ORM model attributes to Pydantic models
    model_config = ConfigDict(from_attributes=True)
    id: int