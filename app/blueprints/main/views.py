
from app.constants import SEASON
from app.enums import Server
from app.extensions import db
from app.models import Player, PlayerStatistics, RunningMatch
from flask import Blueprint, abort, request
from flask.templating import render_template
from flask_babel import gettext
from sqlalchemy import or_

bp = Blueprint("main", __name__)


@bp.route("/", methods=["GET"])
def index():
    return render_template("main/index.html")


@bp.route("/ranking/<server>", methods=["GET"])
def ranking(server: str):
    if server not in ["bergruen", "luxplena"]:
        abort(404)

    season = request.args.get("season", SEASON)
    server: Server = Server(server)
    if server == server.bergruen:
        title = gettext("Ranking Bergruen")
    else:
        title = gettext("Ranking LuxPlena")

    # Query players
    query = (
        db.session.query(
            Player, PlayerStatistics
        ).join(
            PlayerStatistics
        ).filter(
            Player.exists,
            Player.server == server,
            PlayerStatistics.season == season,
            or_(
                PlayerStatistics.wins > 0,
                PlayerStatistics.losses > 0,
                PlayerStatistics.draws > 0,
            ),
        ).order_by(
            PlayerStatistics.points.desc(),
            Player.username.desc(),
        )
    )
    players = query.all()

    return render_template(
        "main/ranking.html",
        title=title,
        server=server.value,
        players=players,
    )


@bp.route("/matches/<server>/", methods=["GET"])
def matches(server: str):
    if server not in ["bergruen", "luxplena"]:
        abort(404)

    server: Server = Server(server)
    if server == server.bergruen:
        title = gettext("Matches Bergruen")
    else:
        title = gettext("Matches LuxPlena")

    matches = (
        db.session.query(
            RunningMatch
        ).filter(
            RunningMatch.server == server,
        ).all()
    )

    return render_template(
        "main/matches.html",
        title=title,
        server=server.value,
        matches=matches,
    )
