import typing

import requests
from dotenv import load_dotenv

from app import create_app
from app.constants import SEASON
from app.enums import CharacterClass, Server
from app.extensions import db
from app.models import Player, PlayerStatistics

FLANDRIA_PLAYERS_CLASS_TO_ENUM = {
    "N": CharacterClass.noble,
    "K": CharacterClass.magic_knight,
    "M": CharacterClass.court_magician,

    "W": CharacterClass.mercenary,
    "G": CharacterClass.gladiator,
    "D": CharacterClass.guardian_swordsman,

    "S": CharacterClass.saint,
    "P": CharacterClass.priest,
    "A": CharacterClass.shaman,

    "E": CharacterClass.explorer,
    "B": CharacterClass.excavator,
    "H": CharacterClass.sniper,
}


if __name__ == "__main__":
    load_dotenv()

    url = "https://www.flandria.info/api/ranking/players?min_lv_land=85"
    with requests.get(url) as req:
        if not req.status_code == 200:
            raise Exception(
                f"Flandria player query not 200 - {req.status_code}")

        players_data = req.json()

    print(f"Got {len(players_data)} players from flandria")

    # Create app to insert into database
    app = create_app(development=True)

    deleted_count = 0

    with app.app_context():
        players = Player.query.filter(Player.exists).all()
        print(f"Looking to update {len(players)} players")

        for player_db in players:
            player_db: Player

            for i, player_ranking in enumerate(players_data):
                player_ranking: typing.Dict[str, typing.Any]

                # Check if the player from the database is somewhere
                # in the ranking.
                # To do so, check for same server and name
                player_db_server = player_db.server.value
                player_ranking_server = (
                    player_ranking["server"]["name"].lower())

                if (player_db.username == player_ranking["name"]
                        and player_db_server == player_ranking_server):

                    # Update player attributes
                    player_db.level_land = player_ranking["level_land"]
                    player_db.level_sea = player_ranking["level_sea"]
                    player_db.guild = player_ranking["guild"]
                    player_db.character_class = (
                        FLANDRIA_PLAYERS_CLASS_TO_ENUM[
                            player_ranking["character_class"]["value"]]
                    )

                    # Delete ranking player obj from list, so that only not
                    # yet entered players exist in the list after all players
                    # are run.
                    del players_data[i]
                    break

            else:
                # loop run through without finding a player -> set it to
                # non existent
                player_db.exists = False
                deleted_count += 1

        print(f"'Deleting' {deleted_count} players, "
              f"updated {len(players) - deleted_count}")

        # Add all new players to the database
        if players_data:
            new_players: typing.List[Player] = []
            for player in players_data:
                # Parse flandria data and adjust it for the flo league model
                new_players.append(Player(**{
                    "username": player["name"],
                    "guild": player["guild"],
                    "character_class": (
                        FLANDRIA_PLAYERS_CLASS_TO_ENUM[
                            player["character_class"]["value"]]
                    ),
                    "server": Server[player["server"]["name"].lower()],
                    "level_land": player["level_land"],
                    "level_sea": player["level_sea"],
                }))

            print(f"Adding {len(new_players)} new players")

            db.session.add_all(new_players)
            db.session.commit()

        # Create statistics object for each player for the current
        # season
        player_statistics: typing.List[PlayerStatistics] = []

        # Queries all players that do not have a player statistics object
        # for the current season
        query = (
            db.session.query(
                Player
            ).filter(
                Player.id.notin_(
                    [p[0] for p in PlayerStatistics.query.filter(
                        PlayerStatistics.season == SEASON,
                    ).with_entities(PlayerStatistics.player_id).all()]
                ),
                Player.exists,
            )
        )

        for player in query.all():
            player_statistics.append(PlayerStatistics(
                player_id=player.id,
                season=SEASON,
            ))

        print("Creating player statistics for "
              f"{len(player_statistics)} players")

        db.session.add_all(player_statistics)
        db.session.commit()
