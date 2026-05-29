from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.database import init_db
from app import models


@asynccontextmanager
async def lifespan(app: FastAPI):
    # startup
    await init_db()

    # shutdown
    yield
    
app = FastAPI(lifespan=lifespan)



@app.get("/health")
async def get_health():
    return {"status": "ok"}