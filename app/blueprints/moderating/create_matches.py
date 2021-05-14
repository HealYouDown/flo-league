import random
import typing

from app.enums import CharacterClass, Server
from app.extensions import db
from app.models import Player, RunningMatch, RunningMatchParticipant
from flask import abort

CLASS_VALUE = {
    CharacterClass.noble: 0,
    CharacterClass.magic_knight: 0,
    CharacterClass.court_magician: 0,

    CharacterClass.explorer: 1,
    CharacterClass.excavator: 1,
    CharacterClass.sniper: 1,

    CharacterClass.saint: 2,
    CharacterClass.shaman: 2,
    CharacterClass.priest: 2,

    CharacterClass.mercenary: 3,
    CharacterClass.gladiator: 3,
    CharacterClass.guardian_swordsman: 3,
}

MATCH = typing.Tuple[typing.List[Player], typing.List[Player]]
MATCHES_LIST = typing.List[MATCH]
USED_PLAYERS = typing.List[Player]
LEFTOVER_PLAYERS = typing.List[Player]


def generate_matches(
    players: typing.List[Player],
    team_size: int,
    make_teams_fair: bool,
) -> typing.Tuple[USED_PLAYERS, LEFTOVER_PLAYERS, MATCHES_LIST]:
    num_matches = len(players) // (team_size * 2)

    matches: typing.List[MATCH] = []
    used_players: LEFTOVER_PLAYERS = []

    for _ in range(num_matches):
        match: MATCH = [[], []]

        for _ in range(team_size):
            for i in range(2):
                for player in players:
                    # make_teams_fair:
                    # Check if the current character class is already
                    # in the team for the match, if that's the case
                    # try to add another class
                    if make_teams_fair:
                        if not any(CLASS_VALUE[p.character_class] == CLASS_VALUE[player.character_class]  # noqa: E501
                                   for p in match[i]):
                            match[i].append(player)

                            # Remove player from the list of players that are
                            # used to fill teams
                            players = [p for p in players if p != player]

                            # Add to used players which are used to fill out
                            # empty teams when there aren't enough
                            # participants
                            used_players.append(player)

                            break
                    else:
                        # unfair teams: just add the next player
                        match[i].append(player)

                        players = [p for p in players if p != player]
                        used_players.append(player)
                        break
                else:
                    # No player matched the criteria for a different class, so
                    # we pick a random one from the available ones
                    player = random.choice(players)
                    match[i].append(player)

                    players = [p for p in players if p != player]
                    used_players.append(player)

        matches.append(match)

    return used_players, players, matches


def create_matches(
    server: Server,
    players: typing.List[Player],
    team_size: int,
    make_teams_fair: bool,
    is_ranked: bool,
) -> None:
    # Check if enough players were given so that at least one
    # match can be created
    if len(players) < team_size * 2:
        abort(400, "Not enough players supplied")

    # Shuffle players
    rng = random.SystemRandom()
    random.shuffle(players, random=rng.random)

    all_matches: MATCHES_LIST = []

    used_players, leftover_players, matches = generate_matches(
        players, team_size, make_teams_fair)
    all_matches.extend(matches)

    # If there are players that are left over (because the team size did
    # did not match the amount of players, try to create teams with those
    # last ones using players that are already in a different match)

    done_leftovers = []

    # if the loop below runs 1000 times, something must have gone wrong
    failsafe_count = 0
    while not all(lp in done_leftovers for lp in leftover_players):
        if failsafe_count == 1000:
            abort(500, "Failed to generate matches. :(")
        failsafe_count += 1

        # shuffle the players that are already participating again
        random.shuffle(used_players, random=rng.random)

        _, _, matches = generate_matches(
            [
                *leftover_players,
                *used_players,
            ],
            team_size,
            make_teams_fair
        )

        # Check all generated matches if the leftover players are now
        # given a match
        for match in matches:
            for team_index in range(2):
                for player in match[team_index]:
                    if player in leftover_players:
                        # leftover player found in a match
                        leftover_players.remove(player)
                        done_leftovers.append(player)
                        used_players.append(player)

                        if match not in all_matches:
                            all_matches.append(match)

    # Check if all players are in the matches
    missing_players = []
    for player in players:
        for match in all_matches:
            if player in match[0] or player in match[1]:
                break
        else:
            missing_players.append(player)

    if missing_players:
        missing_player_list = ", ".join([str(p) for p in missing_players])
        abort(
            500,
            "Somehow we lost a few player: "
            f"{missing_player_list}"
        )

    # Create match database objects
    for match in all_matches:
        match_obj = RunningMatch(
            server=server,
            is_ranked=is_ranked,
        )
        db.session.add(match_obj)
        db.session.flush()

        match_id = match_obj.id
        # Create participants objects
        for index, team in enumerate(match):
            for player in team:
                db.session.add(RunningMatchParticipant(
                    match_id=match_id,
                    team=index,
                    player_id=player.id,
                ))

    db.session.commit()
