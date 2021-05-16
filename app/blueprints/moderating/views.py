from app.utils import add_moderator_log
import itertools
import typing

from app.blueprints.moderating.create_matches import \
    create_matches as create_matches_
from app.blueprints.moderating.forms import CreateMatchesForm, PlayerForm
from app.blueprints.moderating.set_match_winner import \
    set_match_winner as set_match_winner_
from app.blueprints.moderating.utils import delete_match
from app.constants import SEASON
from app.enums import CharacterClass, Server, Winner
from app.extensions import db
from app.models import (FinishedMatch, FinishedMatchParticipant, Log, Player,
                        PlayerStatistics, RunningMatch,
                        RunningMatchParticipant)
from flask import (Blueprint, abort, make_response, redirect, render_template,
                   request, url_for)
from flask_babel import gettext
from flask_login import login_required

bp = Blueprint("moderating", __name__, url_prefix="/moderating")


@bp.route("/")
@login_required
def index():
    players = Player.query.filter(Player.exists).all()

    return render_template(
        "moderating/index.html",
        title=gettext("Moderating"),
        players=players,
    )


@bp.route("/go-to-profile", methods=["POST"])
@login_required
def go_to_profile():
    id = int(request.form.get("id"))

    player = Player.query.get_or_404(id)

    resp = make_response()
    resp.headers["HX-Redirect"] = url_for(
        "main.player_profile",
        server=player.server.value,
        id=player.id
    )

    return resp, 200


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

        team_size = int(form.team_size.data)
        make_teams_fair = form.make_teams_fair.data
        is_ranked = form.is_ranked.data

        add_moderator_log(
            f"Created matches for {server.value} with {len(players)} players"
            f", team_size={team_size}, teams_fair={make_teams_fair}, "
            f"is_ranked={is_ranked}"
        )

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
        ).all()
    ]

    add_moderator_log(
        f"Deleted {len(match_ids)} matches on {server.value}"
    )

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
    match: RunningMatch = RunningMatch.query.get_or_404(match_id)
    server = match.server
    winner: Winner = Winner(winner)

    if match.is_ranked:
        add_moderator_log(
            f"Set match winner for {match} to {winner.name}"
        )

        set_match_winner_(
            match=match,
            winner=winner,
        )
    else:
        add_moderator_log(
            f"Deleted unranked match {match}"
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
        # some matches are left, so just return the 'replace' content
        # for the match element, which is empty as it is
        # removed from the client view.
        return "", 200


@bp.route("/update-match-winner", methods=["POST"])
@login_required
def update_match_winner():
    match_id: int = int(request.args.get("match_id"))
    new_winner: Winner = Winner(int(request.form["match-winner"]))

    match: FinishedMatch = FinishedMatch.query.get_or_404(match_id)

    # Winner did not change
    if new_winner == match.winner:
        resp = make_response()
        resp.headers["HX-Refresh"] = "true"
        return resp, 200

    # Check if the given match is the last one for all participants
    player_ids = []
    for p in itertools.chain(match.team_1, match.team_2):
        player_ids.append(p.player_id)

    for player_id in player_ids:
        last_match = (
            db.session.query(
                FinishedMatch
            ).join(
                FinishedMatchParticipant,
            ).filter(
                FinishedMatchParticipant.player_id == player_id,
            ).order_by(
                FinishedMatch.date.desc()
            ).limit(
                1
            ).first()
        )

        if last_match and last_match is not match:
            return (
                gettext("Not possible!"),
                200
            )

    # Log
    add_moderator_log(
        f"Updated match winner for match {match} from "
        f"{match.winner.name} to {new_winner.name}"
    )

    # Reset the statistics for each player
    players = (
        db.session.query(
            Player, PlayerStatistics,
        ).join(
            PlayerStatistics,
        ).filter(
            Player.id.in_(player_ids),
            PlayerStatistics.season == SEASON,
        ).all()
    )

    participant_objects: typing.List[FinishedMatchParticipant] = []
    for player, statistics in players:
        # Query the last match participant to get the before points
        participant_obj = FinishedMatchParticipant.query.filter(
            FinishedMatchParticipant.player_id == player.id,
            FinishedMatchParticipant.match_id == match.id,
        ).first()
        participant_objects.append(participant_obj)

        statistics.points = participant_obj.points_before

        if match.winner == Winner.draw:
            statistics.draws = statistics.draws - 1

        elif participant_obj.team == 0:
            if match.winner == Winner.team_1:
                statistics.wins = statistics.wins - 1
            else:
                statistics.losses = statistics.losses - 1

        elif participant_obj.team == 1:
            if match.winner == Winner.team_2:
                statistics.wins = statistics.wins - 1
            else:
                statistics.losses = statistics.losses - 1

        # Delete the participant, as we recreate the match more below
        db.session.delete(participant_obj)

    # Delete the old match
    db.session.delete(match)
    db.session.commit()

    # Create a copy of the match and just (re-)set the winner
    # to the new one
    new_match = RunningMatch(
        server=match.server,
        is_ranked=True,
    )
    db.session.add(new_match)
    db.session.flush()

    for p_obj in participant_objects:
        db.session.add(RunningMatchParticipant(
            match_id=new_match.id,
            team=p_obj.team,
            player_id=p_obj.player_id,
        ))

    db.session.commit()

    # Set the match winner to the new winner given to the
    # view function and let the set_match_winner function
    # handle setting the statistics
    set_match_winner_(
        match=new_match,
        winner=new_winner,
    )

    # Delete the running match obj from database
    delete_match(new_match.id, commit_db=True)

    # Return a response that forces a refresh
    resp = make_response()
    resp.headers["HX-Refresh"] = "true"

    return resp, 200


@bp.route("/player/edit/<id>", methods=["GET", "POST"])
@bp.route("/player/add", methods=["GET", "POST"])
@login_required
def edit_or_add_player(id: typing.Optional[int] = None):
    form = PlayerForm()

    if form.validate_on_submit():
        if id:
            player = Player.query.filter(Player.id == int(id),
                                         Player.exists).first()
            if not player:
                abort(404, "Player does not exist")

            player.username = form.username.data
            player.guild = form.guild.data if form.guild.data else None
            player.character_class = CharacterClass(form.character_class.data)
            player.server = Server(form.server.data)
            player.level_land = form.level_land.data
            player.level_sea = form.level_sea.data

            db.session.commit()

            add_moderator_log(
                f"Edit player {player}"
            )

            return redirect(url_for("main.player_profile",
                                    server=player.server.value,
                                    id=player.id))

        else:
            # Check if a player with the given name already exists
            # on the server
            username = form.username.data
            server: Server = Server(form.server.data)

            if Player.query.filter(Player.username == username,
                                   Player.server == server,
                                   Player.exists).count() > 0:
                abort(409, "Player already exists")

            # Create player and statistics object
            player = Player(
                username=username,
                guild=form.guild.data if form.guild.data else None,
                character_class=CharacterClass(form.character_class.data),
                server=server,
                level_land=form.level_land.data,
                level_sea=form.level_sea.data,
            )
            db.session.add(player)
            db.session.flush()

            db.session.add(PlayerStatistics(
                player_id=player.id,
                season=SEASON,
            ))
            db.session.commit()

            add_moderator_log(
                f"Created player {player}"
            )

            return redirect(url_for("main.player_profile",
                                    server=server.value,
                                    id=player.id))

    if id:
        player = Player.query.filter(Player.id == int(id),
                                     Player.exists).first()
        if not player:
            abort(404, "Player does not exist")

        title = f"Edit {player.username}"

        # Pre-populate form
        form.username.data = player.username
        form.guild.data = player.guild
        form.character_class.data = player.character_class.value
        form.server.data = player.server.value
        form.level_land.data = player.level_land
        form.level_sea.data = player.level_sea
    else:
        title = "Add player"

    return render_template(
        "moderating/user_form.html",
        form=form,
        title=title
    )


@bp.route("/logs")
@bp.route("/logs/<int:mod_id>")
@login_required
def logs(mod_id: typing.Optional[int] = None):
    query = Log.query.order_by(Log.date.desc())

    if mod_id:
        query = query.filter(Log.moderator_id == mod_id)

    logs = query.all()

    return render_template("moderating/logs.html",
                           title="Logs",
                           logs=logs)
