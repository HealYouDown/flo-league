from app.models import Moderator


def user_loader(jwt_identity: dict):
    return Moderator.query.filter(Moderator.id == jwt_identity["id"]).first()
