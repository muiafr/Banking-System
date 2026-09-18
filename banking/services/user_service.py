from sqlalchemy import select, or_
from banking.models import User, Deposit, Transaction
from banking.core.errors import ServiceError
from banking.core.security import hash_password
from banking.services.common import get_record, list_records


def get_user(db, user_id):
    return get_record(db, User, user_id)

def list_users(db, nickname=None, email=None, phone_number=None):
    stmt = select(User).order_by(User.id)
    for field, value in [('nickname', nickname), ('email', email), ('phone_number', phone_number)]:
        if value is not None:
            stmt = stmt.where(getattr(User, field) == value)
    return db.scalars(stmt).all()

def create_user(db, data):
    values = data.model_dump()
    values['password'] = hash_password(values['password'])
    user = User(**values)
    db.add(user)
    db.commit()
    return user

def update_user(db, user_id, data):
    user = get_user(db, user_id)
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(user, field, hash_password(value) if field == 'password' else value)
    db.commit()
    return user

def delete_user(db, user_id):
    user = get_user(db, user_id)
    history = db.scalar(select(Deposit.id).where(Deposit.user_id == user_id).limit(1))
    transfers = db.scalar(select(Transaction.id).where(or_(Transaction.sender_id == user_id,
                                                         Transaction.recipient_id == user_id)).limit(1))
    if history is not None or transfers is not None:
        raise ServiceError(409, 'Cannot delete a user with deposit or transaction history')
    db.delete(user)
    db.commit()
