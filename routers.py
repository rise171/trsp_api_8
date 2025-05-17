from fastapi import APIRouter, FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from starlette import status
from sqlalchemy.future import select
from database import make_session
from models import User
from schemas import UserUpdate, UserGet, UserCreate, UserDelete, UserResponse

router = APIRouter(prefix="/user", tags=["Users"])


@router.post("/add", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(user: UserCreate):
    async with make_session() as session:
        db_user = User(
            name=user.name,
            age=user.age,
            role=user.role
        )
        session.add(db_user)
        await session.commit()
        await session.refresh(db_user)
        return db_user


@router.get("/get/{user_id}", response_model=UserResponse)
async def get_user(user_id: int):
    async with make_session() as session:
        result = await session.execute(select(User).where(User.id == user_id))
        db_user = result.scalars().first()
        if db_user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        return db_user


@router.put("/edit/{user_id}", response_model=UserResponse)
async def update_user(user_id: int, user_update: UserUpdate):
    async with make_session() as session:
        result = await session.execute(select(User).where(User.id == user_id))
        db_user = result.scalars().first()
        if db_user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )

        update_data = user_update.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_user, field, value)

        session.add(db_user)
        await session.commit()
        await session.refresh(db_user)
        return db_user


@router.delete("/delete/{user_id}", status_code=status.HTTP_200_OK)
async def delete_user(user_id: int):
    async with make_session() as session:
        result = await session.execute(select(User).where(User.id == user_id))
        db_user = result.scalars().first()
        if db_user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )

        await session.delete(db_user)
        await session.commit()
        return "User are delete"
