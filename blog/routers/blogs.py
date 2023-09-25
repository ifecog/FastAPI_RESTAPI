from fastapi import APIRouter, Depends, status, Response, HTTPException
from sqlalchemy.orm import Session

from .. import models
from ..database import get_db
from blog.schemas import ShowBlog, Blog

router = APIRouter()


@router.post('/blog', status_code=status.HTTP_201_CREATED, tags=['blogs'])
def create_blog(request: Blog, db: Session = Depends(get_db)):
    new_blog = models.Blog(
        title=request.title,
        body=request.body,
        user_id=1
    )
    
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    
    return new_blog


@router.get('/blog', response_model=list[ShowBlog], tags=['blogs'])
def get_blogs(db: Session = Depends(get_db)):
    blogs = db.query(models.Blog).all()
    
    return blogs


@router.get('/blog/{id}', status_code=status.HTTP_200_OK, response_model=ShowBlog, tags=['blogs'])
def get_blog_by_id(id, response: Response, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Blog with the id of {id} not found!')
        
    return blog


@router.put('/blog/{id}', status_code=status.HTTP_202_ACCEPTED, tags=['blogs'])
def update_blog_by_id(id, request: Blog, db: Session = Depends(get_db)):
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
    

@router.delete('/blog/{id}', status_code=status.HTTP_204_NO_CONTENT, tags=['blogs'])
def delete_blog_by_id(id, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'blog with the id of {id} not found'
        )
    
    blog.delete(synchronize_session=False)
    
    db.commit()
    
    return 'Blog post successfully deleted!'
