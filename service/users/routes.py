from fastapi import APIRouter, HTTPException

from users.schemas import(
    UserStartRegisterSchema,

)
from core.database import get_db

from users.models import UserModel

router = APIRouter(tags=["users"], prefix="/users")

@router.post("/register_set_email")
async def register_Set_emal(request: UserStartRegisterSchema):
    pass