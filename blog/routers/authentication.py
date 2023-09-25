from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from .. import models
from ..database import get_db
from blog.schemas import Login
from blog.hashing import Hash


router = APIRouter(
    tags=['authentication']
)

@router.post('/login')
def login(request: Login, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == request.username).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Ivalid email!'
        )
    if not Hash.verify(request.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Incorrect password!'
        )        
        
    return user