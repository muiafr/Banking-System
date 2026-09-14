from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from banking.database import get_db
from banking.models.user import User
from banking.schemas.user import UserCreate

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/")
def get_users(db: Session = Depends(get_db)):
    return db.query(User).all()


@router.get("/{user_id}")
def get_user(user_id: int, db: Session = Depends(get_db)):
    return db.query(User).filter(User.id == user_id).first()

@router.post("/users")
def create_user(
    user: UserCreate,
    db: Session = Depends(get_db)
):
    db_user = User(
        nickname=user.nickname,
        first_name=user.first_name,
        last_name=user.last_name,
        email=user.email,
        phone_number=user.phone_number,
        password=user.password,
        balance=user.balance
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user
