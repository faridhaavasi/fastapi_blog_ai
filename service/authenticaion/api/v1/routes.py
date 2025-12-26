from fastapi import APIRouter, status, Query, Path, Depends, HTTPException, Response

from fastapi.responses import JSONResponse

from sqlalchemy.orm import Session

from service.user.api.v1.models import UserModel, TokenModel

from service.core.database import get_db, mongo_db

from service.core.email_util import send_email

from .schemas import (
    SetEmailInputSchema,
    RegisterFinallySchema,
    SetTokenSchema

)

from service.auth.jwt_auth import (
    get_authenticated_user,
    generate_refresh_token,
    generate_access_token,
    decode_refresh_token,
    generate_verify_token,
    decode_verify_token,
)

router = APIRouter(prefix="/auth/api/v1", tags=["authentication_api_v1"])

@router.post("/register/set_email", status_code=status.HTTP_201_CREATED)
async def set_email(request: SetEmailInputSchema, db: Session = Depends(get_db)):
    input_email = request.email.lower().strip()
    existing = db.query(UserModel).filter_by(email=input_email).first()
    if existing:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="User already registered")

    user = UserModel(email=input_email)
    db.add(user)
    db.commit()
    db.refresh(user)

    verify_token = generate_verify_token(user.id)
    verify_link = f"https://localhost:8000/auth/api/v1/register/verify_email/{verify_token}"

    # save token record (optional but useful)
    token_obj = TokenModel(user_id=user.id, token=verify_token)
    db.add(token_obj)
    db.commit()

    # send email (handle errors)
    try:
        await send_email(subject="Verify your email", recipients=[input_email],
                         body=f"Click to verify: {verify_link}")
    except Exception as e:
        # Option A: rollback token (or mark for retry)
        db.delete(token_obj)
        db.commit()
        # Option B: log and inform client
        raise HTTPException(status_code=500, detail="Failed sending verification email")

    return {"detail": "Verification email sent"}


@router.get("/register/verify_email/{verify_token}")
async def verify_email(verify_token: str, db: Session = Depends(get_db)):
    # if your link is raw token, no need to extract via regex
    user_id = decode_verify_token(verify_token)   # use the dedicated decoder
    # optionally check token exists in DB:
    token_row = db.query(TokenModel).filter_by(token=verify_token).first()
    if not token_row:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Token not found or revoked")

    user = db.query(UserModel).filter_by(id=user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    user.is_verified = True
    db.commit()

    refresh_token = generate_refresh_token(user_id=user_id)


    return {"detail": "Email verified successfully", "refresh_token": refresh_token}


@router.post("/register/finally")
async def register_fin(request: RegisterFinallySchema, response: Response, db: Session = Depends(get_db)):
    try:
        user_id = decode_refresh_token(request.token)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or expired token"
        )

    user_obj = db.query(UserModel).filter_by(id=user_id).first()
    if not user_obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    user_obj.set_password(request.password)

    user_obj.is_active = True

    db.commit()
    db.refresh(user_obj)

    mongo_db.liked_tags.insert_one({'id':user_id, 'tags':[]})


    jwt_access_token = generate_access_token(user_id)
    jwt_refresh_token = generate_refresh_token(user_id)

    response.set_cookie(key='jwt_access_token', value=jwt_access_token)
    response.set_cookie(key='jwt_refresh_token', value=jwt_refresh_token)

    return JSONResponse(
        content={"detail": "Registration completed successfully"},
        status_code=status.HTTP_200_OK
    )


@router.post("/register/set_token", status_code=status.HTTP_200_OK)
async def set_token(request: SetTokenSchema, response: Response, db: Session = Depends(get_db)):
    user = db.query(UserModel).filter_by(email=request.email).one_or_none()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="somthing went wrong"
        )

    if user.verify_password(request.password) is False:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="email or password is wrong"
        )

    jwt_access_token = generate_access_token(user.id)
    jwt_refresh_token = generate_refresh_token(user.id)

    response.set_cookie(
        key='jwt_access_token',
        value=jwt_access_token
    )
    response.set_cookie(
        key='jwt_refresh_token',
        value=jwt_refresh_token
    )

    return {"detail": "tokens are set successfully"}


@router.post("/register/get_token", status_code=status.HTTP_200_OK)
async def set_token(request: SetTokenSchema, db: Session = Depends(get_db)):
    user = db.query(UserModel).filter_by(email=request.email).one_or_none()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="somthing went wrong"
        )

    if user.verify_password(request.password) is False:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="email or password is wrong"
        )

    jwt_access_token = generate_access_token(user.id)

    return JSONResponse(
        content={
            "detail": "Tokens are set successfully",
            "jwt_access_token": jwt_access_token,
        }
    )




