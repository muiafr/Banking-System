import logging
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from banking.core.errors import ServiceError
from banking.routes import users, deposits, transactions

app = FastAPI(title='Banking API', version='1.0.0')
for router in (users.router, deposits.router, transactions.router):
    app.include_router(router)

@app.exception_handler(ServiceError)
async def service_error(request: Request, exc: ServiceError):
    return JSONResponse(status_code=exc.status_code, content={'detail': exc.detail})

@app.exception_handler(IntegrityError)
async def integrity_error(request: Request, exc: IntegrityError):
    return JSONResponse(status_code=409, content={'detail': 'Duplicate user field or related record conflict'})

@app.exception_handler(SQLAlchemyError)
async def database_error(request: Request, exc: SQLAlchemyError):
    logging.getLogger(__name__).error('Database operation failed (%s)', type(exc).__name__)
    return JSONResponse(status_code=503, content={'detail': 'Database operation unavailable'})

@app.get('/health', tags=['Health'])
def health():
    return {'status': 'ok'}
