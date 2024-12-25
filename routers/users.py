from fastapi import APIRouter

router = APIRouter()

@router.post("/register_user/")
async def register_users():
    ...

@router.post("/login_user/")
async def login_user():
    ...
@router.get("/get_user_profile/")
async def get_user_profile():
    ...
@router.put("/edit_user_profile/")
async def edit_user_profile():
    ...