from database.models import (Product, ProductImage)
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import joinedload
from typing import Optional
from database.config import async_session

async def add_product(product_detail: dict, user_id: int):
    async with async_session() as session:
        new_product = Product(
            user_id = user_id,
            product_name = product_detail["product_name"],
            product_category = product_detail["product_category"],
            product_description = product_detail["product_description"],
            product_price = product_detail["product_price"]
        )
        try:
            session.add(new_product)
            await session.commit()
            await session.refresh(new_product)  
            stmt = (
                select(Product)
                .options(joinedload(Product.images))
                .options(joinedload(Product.user))
                .where(Product.product_id == new_product.product_id)
            )
            result = await session.execute(stmt)
            product = result.unique().scalar_one()
            return product
        except IntegrityError as e:
            session.rollback()
            print("Error", e)

async def view_products(product_category: str = "All") -> object:
    async with async_session() as session:
        if product_category == "All":
            stmt = (
                select(Product)
                .options(joinedload(Product.images))
                .options(joinedload(Product.user))
            )
        else:
            stmt = (
                select(Product)
                .options(joinedload(Product.images))
                .options(joinedload(Product.user))
                .filter_by(product_category=product_category)
            )

        result = await session.execute(stmt)
        products = result.unique().scalars().all()
        return products

async def search_products(search_term: str) -> list[Product]:
    async with async_session() as session:
        if search_term == "None":
            stmt = (
                select(Product)
                .options(joinedload(Product.images))
                .options(joinedload(Product.user))
            )
        else:
            stmt = (
                select(Product)
                .options(joinedload(Product.images))
                .options(joinedload(Product.user))
                .where(Product.product_name.ilike(f"%{search_term}%"))
            )
        result = await session.execute(stmt)
        products = result.unique().scalars().all()
        return products


async def user_products(user_id: int) -> list[Product]:
    async with async_session() as session:
        stmt = (
            select(Product)
            .options(joinedload(Product.images))
            .options(joinedload(Product.user))
            .where(Product.user_id == user_id)
        )
        result = await session.execute(stmt)
        products = result.unique().scalars().all() 
        return products

async def add_product_images(product_id: int, user_id: int, image_url: str):
    async with async_session() as session:
        stmt = select(Product).where(
            (Product.product_id == product_id) & (Product.user_id == user_id)
        )
        result = await session.execute(stmt)
        product = result.scalars().first()
        if not product:
            return None
        session.add(ProductImage(product_id = product.product_id, image_url = image_url))
        await session.commit()
        print("Product image added successfully")

async def view_product(product_id: int) -> Optional[Product]:
    async with async_session() as session:
        stmt = (
            select(Product)
            .options(joinedload(Product.images))
            .options(joinedload(Product.user))
            .where(Product.product_id == product_id)
        )
        result = await session.execute(stmt)
        product = result.scalars().first()
        if not product:
            return None
        return product

async def edit_product(prod_detail: dict, prod_id: int, user_id: int):
    async with async_session() as session:
        stmt = select(Product).where(
            (Product.product_id == prod_id) & (Product.user_id == user_id)
        )
        result = await session.execute(stmt)
        product = result.scalars().first()
        product.product_name = prod_detail["product_name"]
        product.product_category = prod_detail["product_category"]
        product.product_description = prod_detail["product_description"]
        await session.commit()
        await session.refresh(product)
async def delete_product(user_id: int, product_id: int):
    async with async_session() as session:

        stmt = select(Product).where(
            (Product.product_id == product_id) & (Product.user_id == user_id)
        )
        result = await session.execute(stmt)
        product = result.scalars().first()
        if not product:
            return None
        await session.delete(product)
        await session.commit()
