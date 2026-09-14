from sqlalchemy import Column, Integer, String, Numeric
from banking.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    nickname = Column(String(50), unique=True, nullable=False)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    phone_number = Column(String(20), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    balance = Column(Numeric(10, 2), default=0)