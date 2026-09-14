from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from banking.database import get_db
from banking.models.deposit import Deposit

router = APIRouter(
    prefix="/deposits",
    tags=["Deposits"]
)


@router.get("/")
def get_deposits(db: Session = Depends(get_db)):
    return db.query(Deposit).all()


@router.get("/{deposit_id}")
def get_deposit(
    deposit_id: int,
    db: Session = Depends(get_db)
):
    return db.query(Deposit).filter(
        Deposit.id == deposit_id
    ).first()