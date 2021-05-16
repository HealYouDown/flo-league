
from app.constants import SEASON
from app.enums import Server
from app.extensions import db
from app.models import (FinishedMatch, FinishedMatchParticipant, Player,
                        PlayerStatistics, RunningMatch)
from flask import Blueprint, abort, request
from flask.globals import current_app
from flask.helpers import send_from_directory
from flask.templating import render_template
from flask_babel import gettext
from sqlalchemy import or_

bp = Blueprint("main", __name__)


@bp.route("/", methods=["GET"])
def index():
    return render_template("main/index.html",
                           title=gettext("Home"))


@bp.route("/robots.txt", methods=["GET"])
def robots():
    return send_from_directory(current_app.static_folder, "robots.txt")


@bp.route("/sitemap.xml", methods=["GET"])
def sitemap():
    return send_from_directory(current_app.static_folder, "sitemap.xml")


@bp.route("/privacy-policy", methods=["GET"])
def privacy_policy():
    return render_template("main/privacy_policy.html",
                           title=gettext("Privacy Policy"))


@bp.route("/legal-notice", methods=["GET"])
def legal_notice():
    return render_template("main/legal_notice.html",
                           title=gettext("Legal Notice"))


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


@bp.route("/players/<server>/<int:id>")
def player_profile(server: str, id: int):
    server: Server = Server(server)
    season = request.args.get("season", SEASON)

    query_res = (
        db.session.query(
            Player, PlayerStatistics
        ).join(
            PlayerStatistics
        ).filter(
            Player.exists,
            Player.id == id,
            PlayerStatistics.season == season,
        ).first()
    )

    if not query_res:
        abort(404, "Player not found")

    player, statistics = query_res

    matches = (
        db.session.query(
            FinishedMatch,
        ).join(
            FinishedMatchParticipant
        ).filter(
            FinishedMatch.season == season,
            FinishedMatchParticipant.player_id == player.id,
        ).order_by(
            FinishedMatch.date.desc()
        ).all()
    )

    return render_template(
        "main/player_profile.html",
        player=player,
        statistics=statistics,
        matches=matches,
        title=gettext("Player %(name)s", name=player.username),
    )
