import json
import sys

from app import create_app
from app.enums import CharacterClassEnum, ServerEnum
from app.extensions import db
from app.helpers import get_utc_time
from app.models import Player
import time

try:
    PLAYER_JSON_FILE = sys.argv[1]
    DEV = False
except IndexError:
    # No path argument -> local
    PLAYER_JSON_FILE = "players.json"
    DEV = True


if __name__ == "__main__":
    start = time.time()
    # Load ranking data
    with open(PLAYER_JSON_FILE, "r") as fp:
        players = {f"{p['server']}.{p['name']}": p for p in json.load(fp)}

    app = create_app(development=DEV)

    with app.app_context():
        # Update existing players
        number_of_players = Player.query.count()
        for index, player_obj in enumerate(Player.query.all()):
            try:
                # Try to get player ranking data
                key = f"{player_obj.server.value}.{player_obj.name}"
                player = players[key]
            except KeyError:
                # Player was not found in ranking
                player_obj.existing = False
                continue

            # Delete found player from ranking data to find out
            # not yet added players
            del players[key]

            # Update player
            for key, value in player.items():
                player_obj.level_land = player["level_land"]
                player_obj.level_sea = player["level_sea"]
                player_obj.guild = player["guild"]
                player_obj.character_class = CharacterClassEnum(
                    player["class_"])
                player_obj.server = ServerEnum(player["server"])
                player_obj.existing = True
                player_obj.updated_on = get_utc_time()

        # All remaining player objects from the ranking are new characters
        new_players = []
        for _, player in players.items():
            new_players.append({
                "server": ServerEnum(player["server"]),
                "name": player["name"],
                "guild": player["guild"],
                "level_land": player["level_land"],
                "level_sea": player["level_sea"],
                "character_class": CharacterClassEnum(player["class_"]),
            })
        db.session.bulk_insert_mappings(Player, new_players)

        # Save changes
        db.session.commit()

    print(f"Took {round(time.time() - start, 2)} seconds to update flo-league db")
