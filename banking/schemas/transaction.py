from datetime import datetime
from pydantic import Field
from banking.schemas.common import PositiveMoney, Request, Response

class TransactionCreate(Request):
    sender_id: int = Field(ge=1)
    recipient_id: int = Field(ge=1)
    amount: PositiveMoney

class TransactionRead(Response):
    id: int
    sender_id: int
    recipient_id: int
    amount: PositiveMoney
    created_at: datetime
