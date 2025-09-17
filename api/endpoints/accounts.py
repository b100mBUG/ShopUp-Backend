from fastapi import APIRouter, HTTPException, File, UploadFile
from api.schemas.users import UserOut, UserIn, UserLogin
from database.actions.upload import upload_image
from pydantic import EmailStr
from database.actions.accounts import view_account, create_account, change_profile_picture, delete_account, edit_account

router = APIRouter()

@router.post("/user-create-account/", response_model=UserOut)
async def create_new_account(user: UserIn):
    user_detail = user.model_dump()
    new_user = await create_account(user_credentials=user_detail)
    return new_user

@router.post("/account-user-login/", response_model=UserOut)
async def login(user: UserLogin):
    account = await view_account(user_details=user.model_dump())
    if not account:
        raise HTTPException(status_code=404, detail="User not found")
    return account

@router.put("/account-edit-profile-picture/")
async def change_profile_photo(user_id: int, file: UploadFile = File(...)):
    image_url = upload_image(file=file)
    await change_profile_picture(user_id = user_id, image_url=image_url)
    return {"message": "Profile picture updated"}

@router.put("/account-edit-profile-details/")
async def change_profile_details(user_id: int, user_name: str, user_email: EmailStr, user_phone: str):
    new_detail = {
        "user_name": user_name,
        "user_email": user_email,
        "user_phone": user_phone
    }
    await edit_account(user_id=user_id, new_detail=new_detail)
    return {"message": "Account updated successfully"}

@router.delete("/account-delete-user-account/")
async def delete_user_account(user_id: int):
    await delete_account(user_id = user_id)
    return {"message": "Account deleted successfully"}

    