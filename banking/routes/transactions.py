from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from banking.database import get_db
from banking.models import Transaction
from banking.schemas.transaction import TransactionCreate, TransactionRead
from banking.services import transaction_service as service

router = APIRouter(prefix='/transactions', tags=['Transactions'])

@router.get('/', response_model=list[TransactionRead])
def list_transactions(db: Session = Depends(get_db)):
    return service.list_records(db, Transaction)

@router.post('/', response_model=TransactionRead, status_code=201)
def create_transaction(data: TransactionCreate, db: Session = Depends(get_db)):
    return service.create_transaction(db, data)

@router.get('/{record_id}', response_model=TransactionRead)
def get_transaction(record_id: int, db: Session = Depends(get_db)):
    return service.get_record(db, Transaction, record_id)

@router.get('/user/{user_id}', response_model=list[TransactionRead])
def user_transactions(user_id: int, db: Session = Depends(get_db)):
    return service.user_transactions(db, user_id)
