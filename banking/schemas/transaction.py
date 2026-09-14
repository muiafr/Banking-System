from datetime import datetime

from pydantic import BaseModel

class Transaction(BaseModel):
    sender_id: int
    recipient_id: int
    amount: int
    created_at: datetime