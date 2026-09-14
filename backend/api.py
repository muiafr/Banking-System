import uvicorn
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from banking.database import SessionLocal
from banking.models.user import User

app = FastAPI()


def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


@app.get("/users")
def get_users(db: Session = Depends(get_db)):
    return db.query(User).all()


@app.get("/users/{user_id}")
def get_user(user_id: int, db: Session = Depends(get_db)):
    return db.query(User).filter(User.id == user_id).first()


if __name__ == '__main__':
    uvicorn.run(app, host="127.0.0.1", port=8000)