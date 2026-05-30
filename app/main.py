from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.database import init_db

from app.routers import gear

@asynccontextmanager
async def lifespan(app: FastAPI):
    # startup
    await init_db()

    # shutdown
    yield
    
app = FastAPI(lifespan=lifespan)

app.include_router(gear.router)



@app.get("/health")
async def get_health():
    return {"status": "ok"}