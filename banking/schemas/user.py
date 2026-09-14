from pydantic import BaseModel, EmailStr, Field


class UserCreate(BaseModel):
    nickname: str = Field(min_length=1, max_length=50)
    first_name: str = Field(min_length=1, max_length=50)
    last_name: str = Field(min_length=1, max_length=50)
    email: EmailStr
    phone_number: str = Field(min_length=7, max_length=10)
    password: str = Field(min_length=8)
    balance: float = Field(ge = 0)