import random
import secrets
from typing import List, Tuple

from app.constants import K
from app.enums import ServerEnum


def create_matches(server: str, players: List) -> List:
    system_random = secrets.SystemRandom()

    # Shuffle list
    random.shuffle(players, random=system_random.random)

    if not len(players) % 2 == 0:
        # Uneven number of players
        # Choose a random player (except the last one)
        # that will fight against last player in list
        players.append(secrets.choice(players[:-1]))

    # Match players
    matches = []
    for p1, p2 in zip(*[iter(players)] * 2):
        matches.append({
            "server": getattr(ServerEnum, server),
            "player_1_id": p1.id,
            "player_2_id": p2.id
        })

    return matches


def calculate_elo(
    player_1_points: int,
    player_2_points: int,
    draw: bool = False
) -> Tuple[int, int]:
    """Returns elo changes for given players. player_1 is supposed
    to be the winner.

    As K is 50, maximum returned value is 50 and -50."""

    if draw:
        win = 0.5
        loss = 0.5
    else:
        win = 1
        loss = 0

    expected_score_player_1 = (
        1 / (1 + 10 ** ((player_2_points - player_1_points)/400)))

    expected_score_player_2 = (
        1 / (1 + 10 ** ((player_1_points - player_2_points)/400)))

    p1_points_change = int(K * (win - expected_score_player_1))

    p2_points_change = int(K * (loss - expected_score_player_2))

    return p1_points_change, p2_points_change
