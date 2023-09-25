from fastapi import APIRouter, Depends, status, Response, HTTPException
from sqlalchemy.orm import Session

from .. import models
from ..database import get_db
from blog.hashing import Hash
from blog.schemas import User, ShowUser

router = APIRouter()


@router.post('/user', status_code=status.HTTP_201_CREATED, response_model=ShowUser, tags=['users'])
def create_user(request: User, db: Session = Depends(get_db)):
    new_user = models.User(
        name=request.name,
        email=request.email,
        password=Hash.bcrypt(request.password)
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return new_user


@router.get('/user', status_code=status.HTTP_202_ACCEPTED, response_model=ShowUser, tags=['users'])
def get_user_by_id(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'User with the id of {id} not found!'
        )
        
    return user
