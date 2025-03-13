from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.crud.user import get_user, create_user, update_user, delete_user
from src.databases.database import get_db
from src.schemas.user import UserCreate, UserList, UserUpdate

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/", response_model=UserList)
async def create_new_user(user: UserCreate, db: AsyncSession = Depends(get_db)):
    db_user = await create_user(db, user)
    if db_user is None:
        raise HTTPException(status_code=400, detail="User with this email already exists")
    return db_user


@router.get("/{user_id}", response_model=UserList)
async def read_user(user_id: int, db: AsyncSession = Depends(get_db)):
    user = await get_user(db, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.put("/{user_id}", response_model=UserList)
async def update_existing_user(user_id: int, user_update: UserUpdate, db: AsyncSession = Depends(get_db)):
    updated_user = await update_user(db, user_id, user_update)
    if updated_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return updated_user


@router.delete("/{user_id}")
async def delete_existing_user(user_id: int, db: AsyncSession = Depends(get_db)):
    deleted_user = await delete_user(db, user_id)
    if deleted_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return {"detail": "User deleted"}
