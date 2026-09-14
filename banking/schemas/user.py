from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    nickname: str
    first_name: str
    last_name: str
    email: EmailStr
    phone_number: str
    password: str
    balance: float