# pip dependencies
import time
from fastapi.responses import PlainTextResponse, JSONResponse
from fastapi import FastAPI, Depends, HTTPException, Request, APIRouter
import logging
import uvicorn
import databases
import inspect
# local dependencies
from config.session_factory import SessionLocal, SQLALCHEMY_DATABASE_URL
from api.api import api_router
from utils.app_middleware import token_decoder
from error_handle.global_handler import RouteErrorHandler

logger = logging.getLogger()
app = FastAPI()
app.include_router(api_router, prefix="/v1")
router = APIRouter(route_class=RouteErrorHandler)
app.include_router(router)
database = databases.Database(SQLALCHEMY_DATABASE_URL)


@app.exception_handler(Exception)
async def Exception_handler(request, exc):
    print(dir(exc))


    if not hasattr(exc, 'status_code'): # 예외처리 가 안된 error는 console 상의 메세지 띄우기
        return PlainTextResponse(str(exc), status_code=500)
    if hasattr(exc, '__cause__'):
        if hasattr(exc, 'dev'): # custom exception 처리
            exc.set_cause(exc.__cause__)
            return JSONResponse(status_code=exc.status_code, content=exc.content)
        return JSONResponse(content=exc.__cause__)
    return JSONResponse(exc)


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
