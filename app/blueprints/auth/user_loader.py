from app.models import Moderator


def load_user(user_id: int):
    return Moderator.query.get(user_id)
