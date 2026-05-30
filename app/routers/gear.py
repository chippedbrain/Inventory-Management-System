from fastapi import APIRouter, Depends, HTTPException
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select

from app.models import GearItem
from app.database import get_session

router = APIRouter(
    prefix="/gear",
    tags=["gear"]
)

@router.post("/", response_model=GearItem)
async def create_gear_item(gear_item: GearItem, session: AsyncSession = Depends(get_session)):
    session.add(gear_item)
    await session.commit()
    await session.refresh(gear_item)
    return gear_item

@router.get("/", response_model=list[GearItem])
async def get_gear_items(session: AsyncSession = Depends(get_session)):
    gear_items = await session.exec(select(GearItem))
    return gear_items.all()

@router.get("/{id}", response_model=GearItem)
async def get_gear_item(id: int, session: AsyncSession = Depends(get_session)):
    gear_item = await session.get(GearItem, id)
    if not gear_item:
        raise HTTPException(status_code=404, detail="Item not found")
    return gear_item

@router.delete("/{id}")
async def delete_gear_item(id: int, session: AsyncSession = Depends(get_session)):
    gear_item = await session.get(GearItem, id)
    if not gear_item:
        raise HTTPException(status_code=404, detail="Item not found")
    await session.delete(gear_item)
    await session.commit()
    return {"detail": "Item deleted"}