from fastapi import APIRouter, status, Query, Path, Depends, HTTPException

from fastapi.responses import JSONResponse

from sqlalchemy.orm import Session

from service.user.api.v1.models import UserModel

from service.core.database import get_db

from service.core.email_util import send_email

from .schemas import SetEmailInputSchema

from service.auth.jwt_auth import (
    get_authenticated_user,
    generate_refresh_token,
    generate_access_token,
    decode_refresh_token,

)

router = APIRouter(prefix="/auth/api/v1", tags=["authentication_api_v1"])


@router.post("/register/set_email")
async def set_email(request: SetEmailInputSchema, db: Session=Depends(get_db)):
    input_email_user = request.email
    user_obj = (db.query(UserModel).filter_by(email=input_email_user).first())
    if user_obj:
        raise HTTPException(
            status_code=status.HTTP_302_FOUND,
            detail="you are registered",
        )
    user_obj = UserModel(email=input_email_user)
    db.add(user_obj)
    db.commit()
    db.refresh(user_obj)
    refresh_token = generate_refresh_token(user_obj.id)
    await send_email(subject="verify email", recipients=[str(input_email_user)],
               body=f"press link{refresh_token}"
    )
    return JSONResponse(content={"detail": "Email has been sent"})


