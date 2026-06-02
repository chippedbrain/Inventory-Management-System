from fastapi import APIRouter, HTTPException, Depends
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select

from app.models import Job, JobCreate
from app.database import get_session

router = APIRouter(
    prefix="/jobs",
    tags=["jobs"]
)

@router.post("/", response_model=Job)
async def create_job(job_data: JobCreate, session: AsyncSession = Depends(get_session)):
    job = Job.model_validate(job_data)
    session.add(job)
    await session.commit()
    await session.refresh(job)
    return job

@router.get("/", response_model=list[Job])
async def get_jobs(session: AsyncSession = Depends(get_session)):
    jobs = await session.exec(select(Job))
    return jobs.all()

@router.get("/{id}", response_model=Job)
async def get_job(id: int, session: AsyncSession = Depends(get_session)):
    job = await session.get(Job, id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return job

@router.delete("/{id}")
async def delete_job(id: int, session: AsyncSession = Depends(get_session)):
    job = await session.get(Job, id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    await session.delete(job)
    await session.commit()
    return {"detail": "Job deleted"}