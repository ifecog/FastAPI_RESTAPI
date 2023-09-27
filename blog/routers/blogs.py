from fastapi import APIRouter, Depends, status, Response, HTTPException
from sqlalchemy.orm import Session

from .. import models
from ..database import get_db
from ..oauth2 import get_current_user
from blog.schemas import ShowBlog, Blog, User
from blog.repository import blog

router = APIRouter(
    prefix='/blog',
    tags=['blogs']
)


@router.post('/', status_code=status.HTTP_201_CREATED)
def create_blog(request: Blog, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return blog.create(request, db)


@router.get('/', response_model=list[ShowBlog])
def get_blogs(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return blog.get_all(db)


@router.get('/{id}', status_code=status.HTTP_200_OK, response_model=ShowBlog)
def get_blog_by_id(id, response: Response, db: Session = Depends(get_db)):
    return blog.get_blog(id, db)


@router.put('/{id}', status_code=status.HTTP_202_ACCEPTED)
def update_blog_by_id(id, request: Blog, db: Session = Depends(get_db)):
    return blog.update(id, request, db)
    

@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_blog_by_id(id, db: Session = Depends(get_db)):
    return blog.destroy(id, db)
