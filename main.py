# pip dependencies
import time
from fastapi.responses import PlainTextResponse
from fastapi import FastAPI, Depends, HTTPException, Request
import logging
import uvicorn
import databases
# local dependencies
from config.session_factory import SessionLocal, SQLALCHEMY_DATABASE_URL
from api.api import api_router
from utils.app_middleware import token_decoder

logger = logging.getLogger()
app = FastAPI()
app.include_router(api_router, prefix="/v1")
database = databases.Database(SQLALCHEMY_DATABASE_URL)


@app.exception_handler(Exception)
async def Exception_handler(request, exc):
    return PlainTextResponse(str(exc), status_code=exc.status_code)


@app.middleware("http")
async def http_role_filter(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers['X-Process-Time'] = str(process_time)
    if "v1/admins" in request.url.path:
        token = request.headers.get("Authorization").split(" ")[-1]
        print('token', token)
        token_data = await token_decoder(token)
        if token_data is None:
            return HTTPException(
                status_code=403, detail="forbidden"
            )
        if not token_data.is_superuser:
            return HTTPException(
                status_code=403, detail="forbidden"
            )
    return response


@app.middleware("http")
async def just_filter(request: Request, call_next):
    response = await call_next(request)
    return response


def get_db2():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
# Dependency


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True, workers=2)
