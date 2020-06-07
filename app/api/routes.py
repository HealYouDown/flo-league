from flask import Blueprint, abort, current_app, jsonify, request
from flask_jwt_extended import (create_access_token, get_current_user,
                                jwt_optional, jwt_required)
from sqlalchemy import or_
from werkzeug.exceptions import HTTPException

from app.api.matchmaking import calculate_elo, create_matches
from app.enums import CharacterClassEnum, MatchWinnerEnum, ServerEnum
from app.extensions import db
from app.models import ActiveMatch, Match, Moderator, Player
from app.api.helpers import add_log

api_bp = Blueprint(__name__, "api", url_prefix="/api")


@api_bp.errorhandler(HTTPException)
def errorhandler(exception):
    return jsonify({
        "msg": str(exception),
    }), exception.code


@api_bp.after_request
def after_request(response):
    # Enable cors in debug mode
    if current_app.config.get("ENV") == "development":
        response.headers.add("Access-Control-Allow-Origin", "*")
        response.headers.add("Access-Control-Allow-Headers", "*")
        response.headers.add("Access-Control-Allow-Methods", "*")
        response.headers.add("Access-Control-Allow-Credentials", True)
    return response


@api_bp.route("/ranking/<string:server>", methods=["GET"])
def ranking(server: str):
    # Returns ranking data
    assert server in ["bergruen", "luxplena"], abort(404)

    query = Player.query.filter(
        or_(Player.wins >= 1,
            Player.losses >= 1,
            Player.draws >= 1,
            ),
        Player.server == getattr(ServerEnum, server))

    return jsonify([p.to_dict(minimal=True) for p in query.all()]), 200


@api_bp.route("/active_matches/<string:server>",
              methods=["GET", "POST", "DELETE"])
@api_bp.route("/active_matches/<string:server>/<int:id>",
              methods=["PATCH"])
@jwt_optional
def active_matches(server: str, id: int = None):
    assert server in ["bergruen", "luxplena"], abort(404)

    if request.method in ["POST", "PATCH", "DELETE"]:
        # Check if endpoint can be accessed
        user = get_current_user()
        if user is None:
            return abort(401)

    # Returns all active matches for given server
    if request.method == "GET":
        query = ActiveMatch.query.filter(
            ActiveMatch.server == getattr(ServerEnum, server))
        return jsonify([match.to_dict() for match in query.all()]), 200

    # Adds active matches to database for given server
    elif request.method == "POST":
        # Check if there are some matches for the given server
        if (ActiveMatch.query
                .filter(ActiveMatch.server == getattr(ServerEnum, server))
                .count()) >= 1:
            return jsonify({
                "msg": f"There are active matches for {server}"
            }), 423
        # Add new matches
        else:
            player_ids = request.json.get("ids")
            players = Player.query.filter(Player.id.in_(player_ids)).all()

            if len(players) == 1:
                return abort(404)

            matches = create_matches(server, players)
            db.session.bulk_insert_mappings(ActiveMatch, matches)
            db.session.commit()

            log_msg = (f"Created matches for {server} "
                       f"with {len(players)} players.")
            add_log(user, log_msg)

            return jsonify({"msg": "Created"}), 201

    # Sets winner of active match (PATCH probably is not the right
    # method, but who cares)
    elif request.method == "PATCH":
        active_match = ActiveMatch.query.filter(
            ActiveMatch.id == id).first_or_404()
        winner = MatchWinnerEnum(int(request.json.get("winner", None)))

        if active_match is None:
            return jsonify({"msg": "Match does no longer exist."}), 404

        if winner is None:
            return jsonify({"msg": "Missing required field 'winner'."}), 422

        player_1 = active_match.player_1
        player_2 = active_match.player_2

        # Calculate elo changes
        if winner == MatchWinnerEnum.player_1:
            p1_change, p2_change = calculate_elo(player_1.points,
                                                 player_2.points)
            # Update player stats
            player_1.wins += 1
            player_2.losses += 1

        elif winner == MatchWinnerEnum.player_2:
            p2_change, p1_change = calculate_elo(player_2.points,
                                                 player_1.points)
            # Update player stats
            player_1.losses += 1
            player_2.wins += 1

        elif winner == MatchWinnerEnum.draw:
            p1_change, p2_change = calculate_elo(player_1.points,
                                                 player_2.points,
                                                 draw=True)
            # Update player stats
            player_1.draws += 1
            player_2.draws += 1

        # Create match
        match = Match(
            server=active_match.server,
            winner=MatchWinnerEnum(winner),
            p1_id=player_1.id,
            p1_name=player_1.name,
            p1_level_land=player_1.level_land,
            p1_level_sea=player_1.level_sea,
            p1_character_class=player_1.character_class,
            p1_points=player_1.points,
            p1_points_change=p1_change,
            p2_id=player_2.id,
            p2_name=player_2.name,
            p2_level_land=player_2.level_land,
            p2_level_sea=player_2.level_sea,
            p2_character_class=player_2.character_class,
            p2_points=player_2.points,
            p2_points_change=p2_change,
        )

        # Update player points
        player_1.points += p1_change
        player_2.points += p2_change

        # Save changes
        db.session.add(match)
        db.session.delete(active_match)
        db.session.commit()

        log_msg = (f"Set winner for match {str(active_match)} "
                   f"to {winner.name}.")
        add_log(user, log_msg)

        return jsonify({"msg": "Success"}), 200

    # Deletes all active matches for given server
    elif request.method == "DELETE":
        for match in ActiveMatch.query.filter(
                ActiveMatch.server == getattr(ServerEnum, server)).all():
            db.session.delete(match)

        db.session.commit()

        log_msg = f"Deleted all matches for {server}"
        add_log(user, log_msg)

        return jsonify({"msg": "Success"}), 200


@api_bp.route("/matches/<int:id>", methods=["PATCH"])
@jwt_required
def matches(id: int):
    user = get_current_user()

    # Updates match winner
    match: Match = Match.query.filter(Match.id == id).first_or_404()

    old_winner = match.winner
    new_winner = MatchWinnerEnum(int(request.json.get("winner")))

    player_1 = Player.query.get(match.p1_id)
    player_2 = Player.query.get(match.p2_id)

    # old winner == new winenr
    if old_winner == new_winner:
        return jsonify({"msg": "Not changed"}), 422

    # old winner: player 1, new winner: p2
    elif (old_winner == MatchWinnerEnum.player_1
          and new_winner == MatchWinnerEnum.player_2):
        p2_change, p1_change = calculate_elo(match.p2_points,
                                             match.p1_points)
        player_1.wins -= 1
        player_1.losses += 1

        player_2.wins += 1
        player_2.losses -= 1

    # old winner: player 1, new winner: draw
    elif (old_winner == MatchWinnerEnum.player_1
          and new_winner == MatchWinnerEnum.draw):
        p1_change, p2_change = calculate_elo(match.p1_points,
                                             match.p2_points,
                                             draw=True)
        player_1.wins -= 1
        player_1.draws += 1

        player_2.losses -= 1
        player_2.draws += 1

    # old winner: player 2, new winner: p1
    elif (old_winner == MatchWinnerEnum.player_2
          and new_winner == MatchWinnerEnum.player_1):
        p1_change, p2_change = calculate_elo(match.p1_points,
                                             match.p2_points)
        player_1.wins += 1
        player_1.losses -= 1

        player_2.wins -= 1
        player_2.losses += 1

    # old winner: player 2, new winner: draw
    elif (old_winner == MatchWinnerEnum.player_2
          and new_winner == MatchWinnerEnum.draw):
        p1_change, p2_change = calculate_elo(match.p1_points,
                                             match.p2_points,
                                             draw=True)
        player_1.losses -= 1
        player_1.draws += 1

        player_2.wins -= 1
        player_2.draws += 1

    # old winner: draw, new winner: p1
    elif (old_winner == MatchWinnerEnum.draw
          and new_winner == MatchWinnerEnum.player_1):
        p1_change, p2_change = calculate_elo(match.p1_points,
                                             match.p2_points)

        player_1.wins += 1
        player_1.draws -= 1

        player_2.losses += 1
        player_2.draws -= 1

    # old winner: draw, new winner: p2
    elif (old_winner == MatchWinnerEnum.draw
          and new_winner == MatchWinnerEnum.player_2):
        p2_change, p1_change = calculate_elo(match.p2_points,
                                             match.p1_points)

        player_1.losses += 1
        player_1.draws -= 1

        player_2.wins += 1
        player_2.draws -= 1

    # add log
    log_msg = (f"Update winner {str(match)} to {new_winner.name}")
    add_log(user, log_msg)

    # update match object
    match.winner = new_winner
    match.p1_points_change = p1_change
    match.p2_points_change = p2_change

    # Update player points
    player_1.points = match.p1_points + p1_change
    player_2.points = match.p2_points + p2_change

    db.session.commit()

    # Return new user object with success
    from_username = request.environ.get("HTTP_REFERER").split("/")[-1]
    user = Player.query.filter(Player.name == from_username).first()

    return_obj = {
        "msg": "success",
    }

    if user is not None:
        return_obj["user"] = user.to_dict()

    return jsonify(return_obj), 200


@api_bp.route("/players/<string:server>", methods=["GET", "POST"])
@api_bp.route("/players/<string:server>/<string:name>", methods=["GET",
                                                                 "PATCH"])
@jwt_optional
def players(server: str = None, name: str = None):
    if request.method in ["POST", "PATCH"]:
        # Check if endpoint can be accessed
        user = get_current_user()
        if user is None:
            return abort(401)

    if request.method == "GET":
        # Returns player data, either for a given id or 'all' for given server
        if name is not None:
            player = (Player.query
                      .filter(Player.name == name,
                              Player.server == getattr(ServerEnum, server))
                      .first_or_404())
            return jsonify(player.to_dict(minimal=False)), 200

        elif server is not None:
            assert server in ["bergruen", "luxplena"], abort(404)
            min_level = int(request.args.get("min_level", 90))
            query = Player.query.filter(
                Player.server == getattr(ServerEnum, server),
                Player.level_land >= min_level)

            return jsonify([p.to_dict(ultra_mini=True)
                            for p in query.all()]), 200

    elif request.method == "PATCH":
        # Updates player data
        player = (Player.query
                  .filter(Player.name == name,
                          Player.server == getattr(ServerEnum, server))
                  .first_or_404())

        player.level_land = int(request.json.get("level_land",
                                                 player.level_land))
        player.level_sea = int(request.json.get("level_sea",
                                                player.level_sea))

        class_key = request.json.get("character_class",
                                     player.character_class)
        player.character_class = getattr(CharacterClassEnum, class_key)

        log_msg = (f"Update player {str(player)}")
        add_log(user, log_msg)

        db.session.commit()

        return jsonify({"msg": "Success"}), 200

    elif request.method == "POST":
        # Adds new user to db

        # check if data is correct
        # guilds are allowed to be None
        if any(not value for key, value in request.json.items()
               if key != "guild"):
            return jsonify({"msg": "Missing data."}), 422

        name = request.json.get("name", None)
        guild = request.json.get("guild", None)
        level_land = int(request.json.get("level_land", None))
        level_sea = int(request.json.get("level_sea", None))
        character_class = getattr(CharacterClassEnum,
                                  request.json.get("character_class", None))
        server = getattr(ServerEnum,
                         request.json.get("server", None))

        # Check if player exists
        player = (Player.query
                  .filter(Player.name == name,
                          Player.server == server)
                  .first())

        if player is not None:
            return jsonify({"msg": "Player already exists."}), 422

        # Create player
        player = Player(
            name=name,
            guild=guild,
            level_land=level_land,
            level_sea=level_sea,
            character_class=character_class,
            server=server
        )

        db.session.add(player)
        db.session.commit()

        log_msg = (f"Create new player {str(player)}")
        add_log(user, log_msg)

        return jsonify({"msg": "Success"}, 201)


@api_bp.route("/login", methods=["POST"])
def login():
    username = request.json.get("username", None)
    password = request.json.get("password", None)

    if not username:
        return jsonify({"msg": "Username field is missing"}), 422

    if not password:
        return jsonify({"msg": "Password field is missing"}), 422

    mod = Moderator.query.filter(Moderator.username == username).first()

    if mod is None:
        return jsonify({"msg": "User was not found."}), 404

    if mod.password != password:
        return jsonify({"msg": "Passwords do not match"}), 404

    token = create_access_token({
        "id": mod.id,
        "username": mod.username,
        "admin": mod.admin
    })

    return jsonify({"access_token": token}), 200
