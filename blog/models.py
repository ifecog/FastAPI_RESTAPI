from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .database import Base


class Blog(Base):
    __tablename__ = 'blogs'
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, unique=True, index=True)
    body = Column(String, unique=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    
    creator = relationship('User', back_populates='blogs')
    
class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String)
    password = Column(String)
    
    blogs = relationship('Blog', back_populates='creator')

    
# class User(Base):
#     __tablename__ = 'users'
    
#     id = Column(Integer, primary_key=True, index=True)
#     name = Column(String, unique=True, index=True)
#     email = Column(String, unique=True, index=True)
#     password = Column(String, unique=True, index=True)
#     play = Column(String)