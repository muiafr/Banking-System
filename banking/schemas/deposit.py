from datetime import datetime

from pydantic import BaseModel

class Deposit(BaseModel):
    user_id: int
    amount: int
    created_at: datetime