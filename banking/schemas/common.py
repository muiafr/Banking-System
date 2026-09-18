from decimal import Decimal
from typing import Annotated
from pydantic import BaseModel, ConfigDict, Field

Money = Annotated[Decimal, Field(ge=0, max_digits=10, decimal_places=2, allow_inf_nan=False)]
PositiveMoney = Annotated[Decimal, Field(gt=0, max_digits=10, decimal_places=2, allow_inf_nan=False)]

class Request(BaseModel):
    model_config = ConfigDict(extra='forbid')

class Response(BaseModel):
    model_config = ConfigDict(from_attributes=True)
