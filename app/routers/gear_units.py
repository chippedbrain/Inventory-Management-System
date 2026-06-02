from fastapi import APIRouter, Depends, HTTPException
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select

from app.models import GearUnit, GearUnitCreate
from app.database import get_session

router = APIRouter(
    prefix="/gear-units",
    tags=["gear-units"]
)

@router.post("/", response_model=GearUnitCreate)
async def create_gear_unit(gear_unit_data: GearUnitCreate, session: AsyncSession = Depends(get_session)):
    gear_unit = GearUnit.model_validate(gear_unit_data)
    session.add(gear_unit)
    await session.commit()
    await session.refresh(gear_unit)
    return gear_unit

@router.get("/", response_model=list[GearUnit])
async def gear_unit_items(session: AsyncSession = Depends(get_session)):
    gear_unit_items = await session.exec(select(GearUnit))
    return gear_unit_items.all()

@router.get("/{id}", response_model=GearUnit)
async def get_gear_unit(id: int, session: AsyncSession = Depends(get_session)):
    gear_unit_item = await session.get(GearUnit, id)
    if not gear_unit_item:
        raise HTTPException(status_code=404, detail="Item not found")
    return gear_unit_item

@router.delete("/{id}")
async def delete_gear_unit(id: int, session: AsyncSession = Depends(get_session)):
    gear_unit_item = await session.get(GearUnit, id)
    if not gear_unit_item:
        raise HTTPException(status_code=404, detail="Item not found")
    await session.delete(gear_unit_item)
    await session.commit()
    return {"detail": "Item deleted"}