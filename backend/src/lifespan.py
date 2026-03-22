import os
from contextlib import asynccontextmanager

from alembic.config import Config
from fastapi import FastAPI

from alembic import command
from src.crypt import hash_password
from src.db.models import User
from src.db.session import SessionLocal
from src.services.user_service import get_user_by_username


def run_migrations():
    cfg = Config("alembic.ini")
    command.upgrade(cfg, "head")


def ensure_admin_user_exists():
    username = os.environ["DEFAULT_ADMIN_USERNAME"]
    password = os.environ["DEFAULT_ADMIN_PASSWORD"]
    is_enabled = os.environ["DEFAULT_ADMIN_ACCOUNT_ENABLED"].lower() == "true"

    with SessionLocal() as session:
        user = get_user_by_username(session, username=username)
        if user is None:
            user = User(
                username=username,
                password=hash_password(password),
                is_admin=True,
                is_blocked=False,
            )
        user.is_blocked = not is_enabled

        session.add(user)
        session.commit()


@asynccontextmanager
async def lifespan(app: FastAPI):
    # We run those via start.sh now
    # run_migrations()

    # We also dont really need a default admin user anymore
    # ensure_admin_user_exists()
    yield
