from datetime import datetime
from sqlalchemy import select
from banking.models import User, Deposit
from banking.core.errors import ServiceError
from banking.services.common import balance, ensure_capacity, get_record, list_records

def create_deposit(db, data):
    with db.begin():
        user = db.scalar(select(User).where(User.id == data.user_id).with_for_update())
        if user is None:
            raise ServiceError(404, 'User not found')
        updated = balance(user) + data.amount
        ensure_capacity(updated)
        user.balance = updated
        deposit = Deposit(user_id=user.id, amount=data.amount, created_at=datetime.now())
        db.add(deposit)
        db.flush()
    return deposit
