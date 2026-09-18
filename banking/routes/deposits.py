from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from banking.database import get_db
from banking.models import Deposit
from banking.schemas.deposit import DepositCreate, DepositRead
from banking.services import deposit_service as service

router = APIRouter(prefix='/deposits', tags=['Deposits'])

@router.get('/', response_model=list[DepositRead])
def list_deposits(db: Session = Depends(get_db)):
    return service.list_records(db, Deposit)

@router.post('/', response_model=DepositRead, status_code=201)
def create_deposit(data: DepositCreate, db: Session = Depends(get_db)):
    return service.create_deposit(db, data)

@router.get('/{record_id}', response_model=DepositRead)
def get_deposit(record_id: int, db: Session = Depends(get_db)):
    return service.get_record(db, Deposit, record_id)
