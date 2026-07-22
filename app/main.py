from fastapi import Depends, FastAPI
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware

from app.deps import get_current_user
from app.routers import auth, gear, jobs, gear_units, job_gear_units

@asynccontextmanager
async def lifespan(app: FastAPI):
    # shutdown
    yield
    
app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(gear.router, dependencies=[Depends(get_current_user)])
app.include_router(gear_units.router, dependencies=[Depends(get_current_user)])
app.include_router(jobs.router, dependencies=[Depends(get_current_user)])
app.include_router(job_gear_units.router, dependencies=[Depends(get_current_user)])

@app.get("/health")
async def get_health():
    return {"status": "ok"}