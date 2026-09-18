from datetime import datetime
from pydantic import Field
from banking.schemas.common import PositiveMoney, Request, Response

class DepositCreate(Request):
    user_id: int = Field(ge=1)
    amount: PositiveMoney

class DepositRead(Response):
    id: int
    user_id: int
    amount: PositiveMoney
    created_at: datetime
