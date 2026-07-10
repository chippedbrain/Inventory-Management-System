from fastapi import APIRouter, HTTPException, Depends
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select

from app.models import User, UserCreate, UserLogin
from app.database import get_session
from app.core.security import hash_password, verify_password, create_access_token

router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)

@router.post("/register")
async def register(user_data: UserCreate, session: AsyncSession = Depends(get_session)):
    check_user = await session.exec(select(User).where(User.email == user_data.email))
    if check_user.first():
        raise HTTPException(status_code=400, detail="Email already registered")
    
    hashed = hash_password(user_data.password)
    user = User(email=user_data.email, hashed_password=hashed)
    
    check_user = await session.exec(select(User).where(User.email == user.email))
    
    if check_user.first():
        raise HTTPException(status_code=400, detail="Email already registered")
    
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user

@router.post("/login")
async def login(user_data: UserLogin, session: AsyncSession = Depends(get_session)):
    user = await session.exec(select(User).where(User.email == user_data.email))
    user = user.first()
    
    if not user or not verify_password(user_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid email or password")
    
    return {"access_token": create_access_token({"sub": str(user.id)}), "token_type": "bearer"}