from fastapi import APIRouter, Depends, Response
from sqlalchemy.orm import Session
from banking.database import get_db
from banking.schemas.user import UserCreate, UserUpdate, UserRead
from banking.services import user_service as service

router = APIRouter(prefix='/users', tags=['Users'])

@router.get('/', response_model=list[UserRead])
def list_users(nickname: str | None = None, email: str | None = None,
               phone_number: str | None = None, db: Session = Depends(get_db)):
    return service.list_users(db, nickname, email, phone_number)

@router.post('/users', response_model=UserRead, status_code=201, deprecated=True)
@router.post('/', response_model=UserRead, status_code=201)
def create_user(data: UserCreate, db: Session = Depends(get_db)):
    return service.create_user(db, data)

@router.get('/{user_id}', response_model=UserRead)
def get_user(user_id: int, db: Session = Depends(get_db)):
    return service.get_user(db, user_id)

@router.patch('/{user_id}', response_model=UserRead)
def update_user(user_id: int, data: UserUpdate, db: Session = Depends(get_db)):
    return service.update_user(db, user_id, data)

@router.delete('/{user_id}', status_code=204)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    service.delete_user(db, user_id)
    return Response(status_code=204)
