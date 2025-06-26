from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from src.models.user import User
from src.schemas.user import UserUpdate


async def get_user(db: AsyncSession, user_id: int):
    result = await db.execute(select(User).where(User.id == user_id))
    return result.scalar_one_or_none()


async def create_user(db: AsyncSession, username: str, email: str, password: str):
    hashed_password = hash_password(password)

    new_user = User(
        username=username,
        email=email,
        hashed_password=hashed_password,
    )
    db.add(new_user)

    await db.commit()
    await db.refresh(new_user)

    return new_user


async def update_user(db: AsyncSession, user_id: int, user_update: UserUpdate):
    user = await get_user(db, user_id)
    if not user:
        return None

    if user_update.hashed_password:
        user_update.hashed_password = hash_password(user_update.hashed_password)

    for key, value in user_update.dict(exclude_unset=True).items():
        setattr(user, key, value)

    await db.commit()
    await db.refresh(user)
    return user


async def delete_user(db: AsyncSession, user_id: int):
    user = await get_user(db, user_id)
    if not user:
        return None

    await db.delete(user)
    await db.commit()
    return user


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    return pwd_context.hash(password)
