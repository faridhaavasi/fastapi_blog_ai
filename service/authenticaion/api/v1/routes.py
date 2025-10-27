from fastapi import APIRouter

router = APIRouter(prefix="/auth/api/v1")


@router.get("/register/set_email")
async def set_email():
    pass