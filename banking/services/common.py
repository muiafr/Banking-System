from decimal import Decimal
from sqlalchemy import select
from banking.core.errors import ServiceError

MAX_BALANCE = Decimal('99999999.99')

def get_record(db, model, record_id):
    record = db.get(model, record_id)
    if record is None:
        raise ServiceError(404, f'{model.__name__} not found')
    return record

def list_records(db, model):
    return db.scalars(select(model).order_by(model.id)).all()

def balance(user):
    # Legacy schema permits NULL; old rows without a balance behave as zero.
    return user.balance if user.balance is not None else Decimal('0')

def ensure_capacity(value):
    if value > MAX_BALANCE:
        raise ServiceError(409, 'Balance exceeds database capacity')
