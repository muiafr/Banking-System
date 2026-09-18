from typing import Annotated
from pydantic import EmailStr, Field, field_validator, model_validator
from banking.schemas.common import Money, Request, Response

Name = Annotated[str, Field(min_length=1, max_length=50)]
Phone = Annotated[str, Field(pattern=r'^\d{7,15}$')]
Email = Annotated[EmailStr, Field(max_length=100)]
Password = Annotated[str, Field(min_length=8)]

class UserCreate(Request):
    nickname: Name
    first_name: Name
    last_name: Name
    email: Email
    phone_number: Phone
    password: Password
    balance: Money = 0

    @field_validator('password')
    @classmethod
    def strong_password(cls, value):
        if not any(c in '!@#$%^&*' for c in value):
            raise ValueError('Password must include a symbol (!@#$%^&*)')
        return value

class UserUpdate(Request):
    nickname: Name | None = None
    email: Email | None = None
    phone_number: Phone | None = None
    password: Password | None = None

    @model_validator(mode='after')
    def validate_changes(self):
        if not self.model_fields_set or any(getattr(self, k) is None for k in self.model_fields_set):
            raise ValueError('Provide at least one non-null field')
        if self.password is not None:
            UserCreate.strong_password(self.password)
        return self

class UserRead(Response):
    id: int
    nickname: str
    first_name: str
    last_name: str
    email: str
    phone_number: str
    balance: Money | None
