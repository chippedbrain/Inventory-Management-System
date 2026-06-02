from fastapi import APIRouter, HTTPException, Depends
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select

from app.models import JobGearUnit, JobGearUnitCreate, Job, GearUnit, GearUnitStatus, CheckoutStatus
from app.database import get_session

router = APIRouter(
    prefix="/job-gear-units",
    tags=["job-gear-units"]
)

@router.post("/", response_model=JobGearUnitCreate)
async def create_job_gear_unit(job_gear_unit_data: JobGearUnitCreate, session: AsyncSession = Depends(get_session)):
    job_gear_unit = JobGearUnit.model_validate(job_gear_unit_data)

    job = await session.get(Job, job_gear_unit.job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    
    gear_unit = await session.get(GearUnit, job_gear_unit.gear_unit_id)
    if not gear_unit:
        raise HTTPException(status_code=404, detail="Gear unit not found")  
    
    if gear_unit.status != GearUnitStatus.available:
        raise HTTPException(status_code=400, detail="Gear unit is not available")
    
    statement = select(JobGearUnit).where(
    JobGearUnit.gear_unit_id == job_gear_unit.gear_unit_id,
    JobGearUnit.status.in_([CheckoutStatus.reserved, CheckoutStatus.checked_out])
    )
    existing = (await session.exec(statement)).first()
    if existing:
        raise HTTPException(status_code=400, detail="Gear unit is already assigned to an active job")
    
    session.add(job_gear_unit)
    await session.commit()
    await session.refresh(job_gear_unit)
    return job_gear_unit

@router.get("/", response_model=list[JobGearUnit])
async def get_job_gear_units(session: AsyncSession = Depends(get_session)):
    job_gear_units = await session.exec(select(JobGearUnit))
    return job_gear_units.all()

@router.get("/{id}", response_model=JobGearUnit)
async def get_job_gear_unit(id: int, session: AsyncSession = Depends(get_session)):
    job_gear_unit = await session.get(JobGearUnit, id)
    if not job_gear_unit:
        raise HTTPException(status_code=404, detail="Item not found")
    return job_gear_unit

@router.delete("/{id}")
async def delete_job_gear_unit(id: int, session: AsyncSession = Depends(get_session)):
    job_gear_unit = await session.get(JobGearUnit, id)
    if not job_gear_unit:
        raise HTTPException(status_code=404, detail="Item not found")
    await session.delete(job_gear_unit)
    await session.commit()
    return {"detail": "Item deleted"}