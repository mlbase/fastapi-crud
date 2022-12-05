# pip dependencies
from fastapi import FastAPI
import logging
import uvicorn
import databases
from starlette.middleware.authentication import AuthenticationMiddleware
from starlette.responses import JSONResponse

# local dependencies
from config.session_factory import SessionLocal, SQLALCHEMY_DATABASE_URL
from api.api import api_router
from custom_exception.Exceptions import ExceptionBase
from utils.app_middleware import custom_backend

logger = logging.getLogger()
app = FastAPI()
app.add_middleware(AuthenticationMiddleware, backend=custom_backend)
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



@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True, workers=2)
