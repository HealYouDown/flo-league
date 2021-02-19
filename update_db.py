import time

import requests

from app import create_app
from app.enums import CharacterClassEnum, ServerEnum
from app.extensions import db
from app.helpers import get_utc_time
from app.models import Player

# NOTE: Change to False when pushing to github
DEV = False

if __name__ == "__main__":
    # sleep 15s to let flandria update reload
    if not DEV:
        time.sleep(15)

    start = time.time()

    # Load ranking data
    with requests.get("https://www.flandria.info/api/ranking/players?min_lv_land=87") as req:
        players = req.json()

    app = create_app(development=DEV)

    with app.app_context():
        # Update existing players
        for index, player_obj in enumerate(Player.query.all()):
            for j, player in enumerate(players):
                if (player["server"]["name"] == player_obj.server.value
                        and player["name"] == player_obj.name):
                    # update player, as he was found in the ranking
                    for key, value in player.items():
                        player_obj.level_land = player["level_land"]
                        player_obj.level_sea = player["level_sea"]
                        player_obj.guild = player["guild"]
                        player_obj.character_class = CharacterClassEnum(
                            player["character_class"]["name"])
                        player_obj.server = ServerEnum(player["server"]["name"])
                        player_obj.updated_on = get_utc_time()
 
                    # delete player data from the list, so that only players that
                    # are not yet indexed in the database stay
                    del players[j]

        # All remaining player objects from the ranking are new characters
        new_players = []
        for player in players:
            new_players.append({
                "server": ServerEnum(player["server"]["name"]),
                "name": player["name"],
                "guild": player["guild"],
                "level_land": player["level_land"],
                "level_sea": player["level_sea"],
                "character_class": CharacterClassEnum(player["character_class"]["name"]),
            })
        db.session.bulk_insert_mappings(Player, new_players)

        # Save changes
        db.session.commit()

    print(f"Took {round(time.time() - start, 2)} seconds to update flo-league db")
