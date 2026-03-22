from sqlalchemy import select
from sqlalchemy.orm import Session

from src.crypt import hash_password
from src.db.models import User


def get_user(session: Session, *, id: int) -> User | None:
    stmt = select(User).where(User.id == id)
    return session.scalar(stmt)


def get_user_by_username(session: Session, *, username: str) -> User | None:
    stmt = select(User).where(User.username == username)
    return session.scalar(stmt)


def create_user(session: Session, username: str, password: str, is_admin: bool) -> User:
    user = get_user_by_username(session, username=username)
    if user is not None:
        raise ValueError(f"User {username!r} already exists")

    user = User(username=username, password=hash_password(password), is_admin=is_admin)

    session.add(user)
    session.commit()

    return user
