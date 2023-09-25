from fastapi import APIRouter

from blog.schemas import Login


router = APIRouter(
    tags=['authentication']
)

@router.post('/login')
def login(request: Login):
    return 'login'