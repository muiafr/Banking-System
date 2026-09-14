from datetime import datetime

from pydantic import BaseModel, Field


class Transaction(BaseModel):
    sender_id: int = Field(ge = 1)
    recipient_id: int = Field(ge = 1)
    amount: int = Field(ge = 1)
    created_at: datetime = Field(default_factory = datetime.now)