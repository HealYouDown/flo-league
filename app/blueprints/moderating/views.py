from app.blueprints.moderating.create_matches import \
    create_matches as create_matches_
from app.blueprints.moderating.forms import CreateMatchesForm
from app.blueprints.moderating.set_match_winner import \
    set_match_winner as set_match_winner_
from app.blueprints.moderating.utils import delete_match
from app.enums import Server, Winner
from app.extensions import db
from app.models import Player, RunningMatch
from flask import (Blueprint, abort, make_response, redirect, render_template,
                   url_for)
from flask_babel import gettext
from flask_login import login_required

bp = Blueprint("moderating", __name__, url_prefix="/moderating")


@bp.route("/")
@login_required
def index():
    return render_template(
        "moderating/index.html",
        title=gettext("Moderating Overview")
    )


@bp.route("/create-matches/<server>", methods=["GET", "POST"])
@login_required
def create_matches(server: str):
    form = CreateMatchesForm()
    server: Server = Server(server)

    if form.validate_on_submit():
        # Check if matches exist
        matches_count = RunningMatch.query.filter(
            RunningMatch.server == server).count()
        if matches_count > 0:
            abort(423, f"Matches already exist for server {server.value}")

        player_ids = [p.data for p in form.player_ids.entries]
        players = Player.query.filter(
            Player.id.in_(player_ids),
            Player.server == server,
        ).all()

        team_size = int(form.mode_select.data)
        make_teams_fair = form.make_teams_fair.data
        is_ranked = form.is_ranked.data

        print(server, players, team_size, make_teams_fair, is_ranked)

        create_matches_(
            server=server,
            players=players,
            team_size=team_size,
            make_teams_fair=make_teams_fair,
            is_ranked=is_ranked,
        )

        return redirect(url_for("main.matches",
                                server=server.value))

    if server == server.bergruen:
        title = gettext("Create Matches Bergruen")
    else:
        title = gettext("Create Matches LuxPlena")

    query = (
        Player.query.filter(
            Player.server == server,
            Player.level_land >= 100,
        )
    )
    players = [p.to_dict() for p in query.all()]

    return render_template(
        "moderating/create_matches.html",
        title=title,
        server=server.value,
        form=form,
        players=players,
    )


@bp.route("/delete-matches/<server>", methods=["DELETE"])
@login_required
def delete_matches(server: str):
    server: Server = Server(server)

    # Get match ids to delete match participants
    # cascade does not work, so we do it manually
    match_ids = [
        m.id for m in RunningMatch.query.filter(
            RunningMatch.server == server,
        ).distinct()
    ]

    for match_id in match_ids:
        delete_match(match_id, commit_db=False)
    db.session.commit()

    # Forces a refresh on the client with htmx
    resp = make_response()
    resp.headers["HX-Refresh"] = "true"

    return resp, 200


@bp.route("/set-match-winner/<int:match_id>/<int:winner>", methods=["POST"])
@login_required
def set_match_winner(match_id: int, winner: str):
    match: RunningMatch = RunningMatch.query.get(match_id)
    server = match.server
    winner: Winner = Winner(winner)

    if match.is_ranked:
        set_match_winner_(
            match=match,
            winner=winner,
        )

    # Delete the match obj from database
    delete_match(match.id, commit_db=True)

    # Check if there are more matches for the given server,
    # if not, force a reload on the client
    matches_count = RunningMatch.query.filter(
        RunningMatch.server == server,
    ).count()

    if matches_count == 0:
        resp = make_response()
        resp.headers["HX-Refresh"] = "true"

        return resp, 200
    else:
        # matches left, so just return the 'replace' content
        # for the match element, which is empty as it is
        # removed from the client view.
        return "", 200
