from fastapi import APIRouter, HTTPException, File, UploadFile
from api.schemas.products import ProductIn, ProductOut
from typing import List
from api.schemas.users import UserLogin
from database.actions.products import (
    view_products, view_product, user_products, 
    search_products, add_product, add_product_images,
    delete_product, edit_product
)
from database.actions.upload import upload_image

router = APIRouter()

@router.get("/products-view-products/")
async def show_products(category: str = "All"):
    products = await view_products(product_category=category)
    return [{
        "ID": prod.product_id,
        "Name": prod.product_name,
        "Category": prod.product_category,
        "Desc": prod.product_description,
        "Price": prod.product_price,
        "Images": [image for image in prod.images],
        "Owner": prod.user
    } for prod in products]

@router.get("/products-view-single-product/")
async def show_single_product(product_id: int):
    product = await view_product(product_id=product_id)
    return {
        "ID": product.product_id,
        "Name": product.product_name,
        "Category": product.product_category,
        "Desc": product.product_description,
        "Price": product.product_price,
        "Images": [image for image in product.images],
        "Owner": product.user
    }

@router.get("/products-user-products/")
async def show_user_products(user_id: int):
    products = await user_products(user_id=user_id,)
    return [{
        "ID": prod.product_id,
        "Name": prod.product_name,
        "Category": prod.product_category,
        "Desc": prod.product_description,
        "Price": prod.product_price,
        "Images": [image for image in prod.images],
        "Owner": prod.user
    } for prod in products]

@router.get("/products-search-products/")
async def show_search_products(search_term: str = "None"):
    products = await search_products(search_term=search_term)
    return [{
        "ID": prod.product_id,
        "Name": prod.product_name,
        "Category": prod.product_category,
        "Desc": prod.product_description,
        "Price": prod.product_price,
        "Images": [image for image in prod.images],
        "Owner": prod.user
    } for prod in products]

@router.post("/products-add-product")
async def append_product(product_detail: ProductIn, user_id: int):
    product = await add_product(
        product_detail=product_detail.model_dump(),
        user_id=user_id,
    )
    return {
        "ID": product.product_id,
        "Name": product.product_name,
        "Category": product.product_category,
        "Desc": product.product_description,
        "Price": product.product_price,
        "Images": [image for image in product.images],
        "Owner": product.user
    }
@router.put("/products-edit-product/")
async def edit_product_endpoint(prod_id: int, user_id: int, prod_name: str, prod_desc: str, prod_cat: str):
    prod_detail = {
        "product_name": prod_name,
        "product_description": prod_desc,
        "product_category": prod_cat
    }
    await edit_product(prod_detail=prod_detail, prod_id=prod_id, user_id=user_id)
    return {"message": "Product editted succesfully"}

@router.post("/products-add-image/")
async def add_image_to_product(user_id: int, product_id: int, file: UploadFile = File(...)):
    image_url = upload_image(file=file)
    await add_product_images(
        product_id=product_id,
        user_id=user_id,
        image_url=image_url
    )
    return {"message": "Image added succesfully"}

@router.delete("/products-delete/")
async def delete_this_product(user_id: int, product_id: int):
    await delete_product(
        user_id=user_id,
        product_id=product_id
    )
    return {"message": "Product deleted successfully"}

