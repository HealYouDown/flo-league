from fastapi import APIRouter, Depends, Response, status
from fastapi.security import OAuth2PasswordRequestForm
from fastapi_login.exceptions import InvalidCredentialsException
from sqlalchemy.orm import Session

from src.api.deps import get_db, require_user
from src.auth import manager
from src.crypt import verify_password
from src.db.models import User
from src.schemas.user import ReadUser
from src.services.user_service import get_user_by_username

router = APIRouter(prefix="/auth")


@router.post("/login")
async def login_route(
    response: Response,
    data: OAuth2PasswordRequestForm = Depends(),
    session: Session = Depends(get_db),
):
    username = data.username
    password = data.password

    user = get_user_by_username(session, username=username)
    if user is None:
        raise InvalidCredentialsException
    if user.is_blocked:
        raise InvalidCredentialsException
    if not verify_password(password, user.password):
        raise InvalidCredentialsException

    token = manager.create_access_token(
        data={
            "sub": str(user.id),
            "username": user.username,
            "is_admin": user.is_admin,
        }
    )
    response.set_cookie("access_token", value=token, httponly=True, samesite="lax")
    response.status_code = status.HTTP_200_OK
    return response


@router.post("/logout")
async def logout(response: Response):
    response.delete_cookie("access_token", httponly=True, samesite="lax")
    return response


@router.get("/me")
async def get_me_route(
    user: User = Depends(require_user),
) -> ReadUser:
    return ReadUser.model_validate(user)
