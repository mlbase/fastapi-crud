from fastapi import FastAPI, Depends, HTTPException
import uvicorn


# from config.session_factory import SessionLocal, engine
from config.session_factory import SessionLocal
from api.api import api_router

app = FastAPI()


# Dependency
def get_db2():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


if __name__ == "__main__":
    app.include_router(api_router, prefix="/v1")
    uvicorn.run(app, host="0.0.0.0", port=8000)
