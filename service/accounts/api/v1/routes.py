from fastapi import APIRouter, status, Query, Path, Depends, HTTPException, Response

from fastapi.responses import JSONResponse

from sqlalchemy.orm import Session

from service.user.api.v1.models import UserModel, TokenModel



router = APIRouter(prefix="/accounts/api/v1", tags=["accounts_api_v1"])


