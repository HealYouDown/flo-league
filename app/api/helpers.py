from app.models import Moderator, Log
from app.extensions import db


def add_log(user: Moderator, msg: str) -> None:
    log = Log(
        moderator_id=user.id,
        message=msg
    )

    db.session.add(log)
    db.session.commit()
