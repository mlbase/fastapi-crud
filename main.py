import time

from fastapi import FastAPI, Depends, HTTPException, Request
import uvicorn
import databases
from pydantic import ValidationError
from starlette import status

# from config.session_factory import SessionLocal, engine
from config.session_factory import SessionLocal, SQLALCHEMY_DATABASE_URL
from api.api import api_router
from jose import jwt
from jose.exceptions import JWTError
from config.setting import settings
from config import security
from schema.token import TokenPayload

app = FastAPI()
app.include_router(api_router, prefix="/v1")
database = databases.Database(SQLALCHEMY_DATABASE_URL)


@app.middleware("http")
async def http_filter(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers['X-Process-Time'] = str(process_time)
    if "v1/admins" in request.url.path:
        token = request.headers.get("Authorization").split(" ")[-1]
        # print(token)
        try:
            payload = jwt.decode(
                token, settings.SECRET_KEY, algorithms=[security.ALGORITHM]
            )
            token_data = TokenPayload(**payload)
            # print(token_data)
        except ValidationError:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Could not validate credentials"
            )
        except JWTError:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="jwt key가 유효하지 않습니다"
            )

        if not token_data.is_superuser:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="관리자가 아닙니다")
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
