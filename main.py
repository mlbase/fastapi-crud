# pip dependencies
import time

from fastapi import FastAPI, Depends, HTTPException, Request, APIRouter
import logging
import uvicorn
import databases
from starlette.responses import JSONResponse

# local dependencies
from config.session_factory import SessionLocal, SQLALCHEMY_DATABASE_URL
from api.api import api_router
from custom_exception.Exceptions import ExceptionBase
from utils.app_middleware import token_decoder

logger = logging.getLogger()
app = FastAPI()
app.include_router(api_router, prefix="/v1")
database = databases.Database(SQLALCHEMY_DATABASE_URL)


@app.exception_handler(Exception)
async def global_handler(request, exc):

    if isinstance(exc, ExceptionBase):
        # exc.set_content(exc.dev, exc.detail)
        return JSONResponse(status_code=exc.status_code, content=exc.content)
    if not hasattr(exc, 'status_code'): # 예외처리 가 안된 error는 console 상의 메세지 띄우기
        exc_to_custom = ExceptionBase()
        exc_to_custom.status_code = 500
        dev = str(exc)
        detail = "관리자에게 문의하세요"
        exc_to_custom.set_content(dev=dev, detail=detail)
        return JSONResponse(status_code=exc_to_custom.status_code, content=exc_to_custom.content)
    return JSONResponse(status_code=exc.status_code, content=str(exc))

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



@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True, workers=2)
