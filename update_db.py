import json
import sys

from app import create_app
from app.enums import CharacterClassEnum, ServerEnum
from app.extensions import db
from app.helpers import get_utc_time
from app.models import Player

try:
    PLAYER_JSON_FILE = sys.argv[1]
    DEV = False
except IndexError:
    # No path argument -> local
    PLAYER_JSON_FILE = "players.json"
    DEV = True


if __name__ == "__main__":
    # Load ranking data
    with open(PLAYER_JSON_FILE, "r") as fp:
        players: list = json.load(fp)

    app = create_app(development=DEV)

    with app.app_context():
        # Update existing players
        for player_obj in Player.query.all():
            try:
                # Try to get player ranking data
                player = next(filter(
                    lambda p: (p["name"] == player_obj.name
                               and p["server"] == player_obj.server.value),
                    players))
            except StopIteration:
                # Player was not found in ranking
                player_obj.existing = False
                continue

            # Delete found player from ranking data to speed up filtering
            players.remove(player)

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
        for player in players:
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
