import datetime as dt
import os

from fastapi_login import LoginManager

from src.db.models import User
from src.db.session import SessionLocal
from src.services.user_service import get_user

manager = LoginManager(
    os.environ["SECRET_KEY"],
    token_url="/auth/login",
    use_cookie=True,
    cookie_name="access_token",
    default_expiry=dt.timedelta(days=180),
)


@manager.user_loader()
def load_user(sub: str) -> User | None:
    id = int(sub)
    with SessionLocal() as session:
        user = get_user(session, id=id)
        if user is None:
            return None
        if user.is_blocked:
            return None
        return user
