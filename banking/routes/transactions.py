from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from banking.database import get_db
from banking.models.transaction import Transaction

router = APIRouter(
    prefix="/transactions",
    tags=["Transactions"]
)


@router.get("/")
def get_transactions(db: Session = Depends(get_db)):
    return db.query(Transaction).all()


@router.get("/{transaction_id}")
def get_transaction(
    transaction_id: int,
    db: Session = Depends(get_db)
):
    return db.query(Transaction).filter(
        Transaction.id == transaction_id
    ).first()


@router.get("/user/{user_id}")
def get_user_transactions(
    user_id: int,
    db: Session = Depends(get_db)
):
    return db.query(Transaction).filter(
        (Transaction.sender_id == user_id) |
        (Transaction.recipient_id == user_id)
    ).order_by(
        Transaction.created_at.desc()
    ).all()

