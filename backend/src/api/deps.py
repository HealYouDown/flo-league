import typing as t

from fastapi import Depends, HTTPException, status

from src.auth import manager
from src.db.models import User
from src.db.session import SessionLocal

if t.TYPE_CHECKING:
    from sqlalchemy.orm import Session


def get_db() -> t.Generator["Session"]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def require_user(user: User = Depends(manager)):
    if user.is_blocked:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Blocked Account",
        )
    return user


def require_admin(user: User = Depends(require_user)):
    if not user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admins only",
        )
    return user
