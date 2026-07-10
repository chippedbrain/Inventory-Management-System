from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.database import init_db

from app.routers import auth, gear, jobs, gear_units, job_gear_units

@asynccontextmanager
async def lifespan(app: FastAPI):
    # startup
    await init_db()

    # shutdown
    yield
    
app = FastAPI(lifespan=lifespan)

app.include_router(auth.router)
app.include_router(gear.router)
app.include_router(gear_units.router)
app.include_router(jobs.router)
app.include_router(job_gear_units.router)



@app.get("/health")
async def get_health():
    return {"status": "ok"}