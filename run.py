from database.actions.accounts import (
    create_account, view_account, change_profile_picture, delete_account
)
from database.actions.cart import(
     add_to_cart, view_cart, check_out
)
from database.actions.products import (
    add_product, user_products,
    view_products, search_products,
)
import asyncio

def enter_credentials() -> dict:
    user_credentials = {
        "user_name": input("Enter Username: "),
        "user_email": input("Enter Email Address: "),
        "user_phone": input("Enter Phone Number: "),
        "user_id_number": input("Enter ID Number: "),
        "profile_pic_url": input("Enter Image URL: "),
        "user_password": input("Enter Password: ")
    }
    return user_credentials

def enter_product_credentials() -> dict:
    product_credentials = {
        "product_name": input("Enter Product Name: "),
        "product_category": input("Enter Product Category: "),
        "product_description": input("Enter Product Description: "),
        "product_price": float(input("Enter Product Price: ")),
        "product_image_url": input("Enter Product Image URL: ")
    }
    return product_credentials

def enter_details() -> dict:
    user_details = {
        "user_name": input("Enter User Name: "),
        "user_password": input("Enter User Password: ")
    }
    return user_details


async def main():
    actions = [
        "Create Account", "View Account", "Add Product", "View Products", "Search Products",
        "View My Products", "Add to Cart", "View Cart", "Check Out", "Change Profile", "Delete Account"
    ]
    while True:

        for i, action in enumerate(actions, start=1):
            print(f"{i}. {action}")

        act = int(input("Choose action: "))

        if act == 1:
            user_credentials = enter_credentials()
            await create_account(user_credentials=user_credentials)
        elif act == 2:
            user_details = enter_details()
            account = await view_account(user_details=user_details)
            if not account:
                print("Account not found")
                return
            print(f"Name: {account.user_name}\nEmail: {account.user_email}\nPhone: {account.user_phone}")
        elif act == 3:
            product_detail = enter_product_credentials()
            user_details = enter_details()
            await add_product(product_detail=product_detail, user_detail=user_details)
        elif act == 4:
            category = input("Enter Category Of Products You Wanna Search: ")
            if not category.strip():
                category = "All"
            products = await view_products(product_category=category)
            if not products:
                print(f"No product with category {category}")
                continue
            for product in products:
                print(f"Name: {product.product_name}\nCategory: {product.product_category}\nDescription: {product.product_description}\nPrice: {product.product_price}")
        elif act == 5:
            search_term = input("Enter Search Term: ")
            products = await search_products(search_term=search_term)
            for product in products:
                print(f"Name: {product.product_name}\nCategory: {product.product_category}\nDescription: {product.product_description}\nPrice: {product.product_price}")
        elif act == 6:
            user_detail = enter_details()
            products = await user_products(user_details=user_detail)
            if not products:
                print("User has no products")
                continue
            for product in products:
                print(f"Name: {product.product_name}\nCategory: {product.product_category}\nDescription: {product.product_description}\nPrice: {product.product_price}")
        elif act == 7:
            product_id = int(input("Enter Product ID: "))
            await add_to_cart(product_id=product_id, user_detail=enter_details())
        elif act == 8:
            user_detail = enter_details()
            cart_items = await view_cart(user_details=user_detail)
            for item in cart_items:
                product = item.product
                print(f"Product: {product.product_name} @ {product.product_price}")
        elif act == 9:
            user_detail = enter_details()
            check_out_content = await check_out(user_detail=user_detail)
            print(check_out_content)
        elif act == 10:
            user_detail = enter_details()
            image_url = input("Enter Image URL: ")
            await change_profile_picture(user_detail=user_detail, image_url=image_url)
        elif act == 11:
            user_detail = enter_details()
            await delete_account(user_detail=user_detail)

       

if __name__ == "__main__":
    asyncio.run(main())