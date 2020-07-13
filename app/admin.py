from flask import Flask, request, abort, session
from flask_admin.contrib.sqla import ModelView
from flask_jwt_extended import decode_token

from app.extensions import admin, db
from app.models import ActiveMatch, Log, Match, Moderator, Player


class View(ModelView):
    def is_accessible(self) -> bool:
        try:
            if session["admin"]:
                return True
        except KeyError:
            pass

        token = request.args.get("token")
        if token is None:
            return abort(401)

        user = decode_token(token)
        if not user["identity"]["admin"]:
            return False

        session["admin"] = True
        return True


def init_admin(app: Flask) -> None:
    admin.init_app(app)

    # Register views
    admin.add_view(View(ActiveMatch, db.session))
    admin.add_view(View(Log, db.session))
    admin.add_view(View(Match, db.session))
    admin.add_view(View(Moderator, db.session))
    admin.add_view(View(Player, db.session))
