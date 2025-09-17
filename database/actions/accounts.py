from database.config import async_session
from database.models import (User)
from sqlalchemy import select
from typing import Optional
from sqlalchemy.exc import IntegrityError
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=['bcrypt'], deprecated="auto")

# Let's create a user account
async def create_account(user_credentials: dict):
    async with async_session() as session:
        new_user = User(
            user_name = user_credentials["user_name"],
            user_email = user_credentials["user_email"],
            user_phone = user_credentials["user_phone"],
            user_password = pwd_context.hash(user_credentials["user_password"]),
            profile_pic_url = user_credentials["profile_pic_url"]
        )
        try:
            session.add(new_user)
            await session.commit()
            await session.refresh(new_user)
            return new_user
        except IntegrityError as e:
            await session.rollback()
            print("Error", e)

async def view_account(user_details: dict) -> Optional[User]:
    async with async_session() as session:
        stmt = select(User).filter(
            User.user_name == user_details["user_name"]
        )
        result = await session.execute(stmt)
        user = result.scalars().first()
        if not user:
            return None
        if not pwd_context.verify(user_details["user_password"], user.user_password):
            return None
        return user

async def change_profile_picture(user_id: int, image_url: str):
    async with async_session() as session:
        stmt = select(User).where(
            User.user_id == user_id
        )
        result = await session.execute(stmt)
        user = result.scalars().first()
        user.profile_pic_url = image_url
        await session.commit()
        await session.refresh(user)

async def edit_account(user_id: int, new_detail: dict):
    async with async_session() as session:
        stmt = select(User).where(
            User.user_id == user_id
        )
        result = await session.execute(stmt)
        user = result.scalars().first()
        user.user_name = new_detail["user_name"]
        user.user_email = new_detail["user_email"]
        user.user_phone = new_detail["user_phone"]

        await session.commit()
        await session.refresh(user)

async def delete_account(user_id: int):
    async with async_session() as session:
        stmt = select(User).where(
            User.user_id == user_id
        )
        result = await session.execute(stmt)
        user = result.scalars().first()
        await session.delete(user)
        await session.commit()
        return True

