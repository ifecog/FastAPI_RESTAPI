from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from ..database import get_db
from blog.schemas import User, ShowUser
from blog.repository import user

router = APIRouter(
    prefix='/user',
    tags=['users']
)


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=ShowUser)
def create_user(request: User, db: Session = Depends(get_db)):
    return user.create(request, db)


@router.get('/', status_code=status.HTTP_202_ACCEPTED, response_model=ShowUser)
def get_user_by_id(id: int, db: Session = Depends(get_db)):
    return user.get_user(id, db)
