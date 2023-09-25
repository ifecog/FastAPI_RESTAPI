from fastapi import status, HTTPException
from sqlalchemy.orm import Session

from .. import models
from blog.schemas import Blog


def create(request: Blog, db: Session):
    new_blog = models.Blog(
        title=request.title,
        body=request.body,
        user_id=1
    )
    
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    
    return new_blog


def get_all(db: Session):
    blogs = db.query(models.Blog).all()
    
    return blogs


def get_blog(id: int, db: Session):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Blog with the id of {id} not found!')
        
    return blog


def update(id: int, request: Blog, db: Session):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Blog with the id of {id} not found'
        )
    
    # update individual blog attributes
    for key, value in request.__dict__.items():
        setattr(blog, key, value)
       
    db.commit()
    
    return 'Blog details successfuly updated'


def destroy(id: int, db: Session):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'blog with the id of {id} not found'
        )
    
    blog.delete(synchronize_session=False)
    
    db.commit()
    
    return 'Blog post successfully deleted!'