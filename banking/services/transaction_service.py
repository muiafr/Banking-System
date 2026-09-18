from datetime import datetime
from sqlalchemy import select, or_
from banking.models import User, Transaction
from banking.core.errors import ServiceError
from banking.services.common import balance, ensure_capacity, get_record, list_records

def create_transaction(db, data):
    if data.sender_id == data.recipient_id:
        raise ServiceError(400, 'Sender and recipient must be different users')
    with db.begin():
        users = {}
        for user_id in sorted((data.sender_id, data.recipient_id)):
            user = db.scalar(select(User).where(User.id == user_id).with_for_update())
            if user is None:
                raise ServiceError(404, 'Sender or recipient not found')
            users[user_id] = user
        sender, recipient = users[data.sender_id], users[data.recipient_id]
        if balance(sender) < data.amount:
            raise ServiceError(409, 'Insufficient balance')
        updated = balance(recipient) + data.amount
        ensure_capacity(updated)
        sender.balance = balance(sender) - data.amount
        recipient.balance = updated
        transaction = Transaction(**data.model_dump(), created_at=datetime.now())
        db.add(transaction)
        db.flush()
    return transaction

def user_transactions(db, user_id):
    get_record(db, User, user_id)
    return db.scalars(select(Transaction).where(or_(Transaction.sender_id == user_id,
        Transaction.recipient_id == user_id)).order_by(Transaction.created_at.desc(), Transaction.id.desc())).all()
