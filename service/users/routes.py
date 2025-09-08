from fastapi import APIRouter , Depends, responses, HTTPException, status

from users.schmas import SetEmailSchema

from sqlalchemy.orm import Session

from core.database import get_db

from users.models import Usermodel


router = APIRouter(prefix="/users_api", tags=["users_api_v1"])


@router.post("set_email/")
async def set_email(requset: SetEmailSchema):
    return {}