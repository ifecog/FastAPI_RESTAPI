from sqlalchemy import Boolean, Column, ForeignKey, Integer, String

from .database import Base


class Blog(Base):
    __tablename__ = 'blogs'
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, unique=True, index=True)
    body = Column(String, unique=True, index=True)
    
    