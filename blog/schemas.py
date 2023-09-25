from pydantic import BaseModel

# from typing import List       
        
class User(BaseModel):
    name: str
    email: str
    password: str


class BlogBase(BaseModel):
    title: str
    body: str
       
       
class Blog(BlogBase):
    class Config():
        orm_mode = True 
    
class ShowUser(BaseModel):
    name: str
    email: str
    blogs: list[Blog]

    class Config():
        orm_mode = True


class ShowBlog(BaseModel):
    title: str
    body: str
    creator: ShowUser
    
    class Config():
        orm_mode = True
        

class Login(BaseModel):
    username: str
    password: str