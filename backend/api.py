import uvicorn
from fastapi import FastAPI

from banking.routes import users
from banking.routes import transactions
from banking.routes import deposits


app = FastAPI()


app.include_router(users.router)
app.include_router(transactions.router)
app.include_router(deposits.router)


if __name__ == "__main__":
    uvicorn.run(
        app,
        host="127.0.0.1",
        port=8000
    )