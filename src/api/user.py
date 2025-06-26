from typing import Annotated

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from src.crud.user import get_user, create_user, update_user, delete_user
from src.databases.database import get_db
from src.models.user import User
from src.schemas.user import UserCreate, UserList, UserUpdate
from src.services.auth import get_current_user

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/", response_model=UserList, status_code=status.HTTP_201_CREATED)
async def create_new_user(user: UserCreate, db: AsyncSession = Depends(get_db)):
    db_user = await create_user(db, user.username, user.email, user.hashed_password)
    if db_user is None:
        raise HTTPException(
            status_code=400, detail="User with this email already exists"
        )
    return db_user


@router.get("/{user_id}", response_model=UserList)
async def read_user(
    user_id: int,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    user = await get_user(db, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.put("/{user_id}", response_model=UserList)
async def update_existing_user(
    user_id: int,
    user_update: Annotated[UserUpdate, Depends()],
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    updated_user = await update_user(db, user_id, user_update)
    if updated_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return updated_user


@router.delete("/{user_id}")
async def delete_existing_user(
    user_id: int,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    deleted_user = await delete_user(db, user_id)
    if deleted_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return {"detail": "User deleted"}
